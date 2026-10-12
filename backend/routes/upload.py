from fastapi import APIRouter, UploadFile, File
import shutil
import os

from crew.crew_manager import run_crew

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_crew(
        {
            "file_path": file_path
        }
    )

    return {
        "filename": file.filename,
        **result
    }