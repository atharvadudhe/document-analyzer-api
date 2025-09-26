from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.nlp import analyze_text
from typing import Any

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    summary: str
    entities: Any
    keywords: Any

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analyze raw text: produce summary, named entities, and keywords."""
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty")

    result = await analyze_text(request.text)
    return AnalyzeResponse(**result)