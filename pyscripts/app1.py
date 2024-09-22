import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add the current directory to Python path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io

# Import functions from other scripts
from easyocr_test import extract_text_from_image  # Updated import
from llm import process_row
from regex import extract_value_unit

# Debug prints
print("Current working directory:", os.getcwd())
print("Files in the current directory:", os.listdir())

app = FastAPI()

# Create an uploads directory if it doesn't exist
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html") as f:
        return f.read()

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    # Save the uploaded image file
    file_path = os.path.join(uploads_dir, image.filename)
    with open(file_path, "wb") as f:
        contents = await image.read()
        f.write(contents)
    
    return {"filename": image.filename, "url": f"/uploads/{image.filename}"}

@app.post("/inference")
async def inference(image: UploadFile = File(...)):
    # Read the image file
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    
    # Step 1: Extract text using EasyOCR
    easyoutput = extract_text_from_image(img)
    
    # Step 2: Process with LLM
    prompt = "Extract the measurement and unit from the text"
    llmout = process_row(img, easyoutput, prompt)
    
    # Step 3: Extract value and unit using regex
    regoutput = extract_value_unit(llmout)
    
    return JSONResponse(content={"result": regoutput})

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)