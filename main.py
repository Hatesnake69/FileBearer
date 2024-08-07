from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Путь для сохранения файлов
UPLOAD_DIR = "./uploaded_files"

# Убедитесь, что директория для загрузки существует
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_location = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_location):
        return FileResponse(path=file_location, filename=filename, media_type='application/xml')
    else:
        raise HTTPException(status_code=404, detail="File not found")
