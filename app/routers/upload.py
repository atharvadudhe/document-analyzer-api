from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import parse_file
from typing import Dict

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict:
    """Accept a file, parse supported types, and return extracted text."""
    filename = file.filename
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    text = await parse_file(filename, contents)
    if not text or not text.strip():
        raise HTTPException(status_code=422, detail="Unable to extract text from document or document is empty")

    return {"filename": filename, "text": text}