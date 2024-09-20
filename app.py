from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    response = JSONResponse(content={"message": "lkjfdlfjdfl"})
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
