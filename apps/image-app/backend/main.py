from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "/data/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get("/images")
def list_images():
    return os.listdir(UPLOAD_DIR)

app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")