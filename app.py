import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

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
        # aap.inference -> calling three scripts -> easyocr.py -> llm.py -> regex.py -> output. 
    
    return {"filename": image.filename, "url": f"/uploads/{image.filename}"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
