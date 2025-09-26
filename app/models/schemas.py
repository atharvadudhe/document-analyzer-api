from pydantic import BaseModel
from typing import List, Dict

class UploadResponse(BaseModel):
    filename: str
    text: str

class EntityItem(BaseModel):
    text: str
    label: str

class AnalyzeResponse(BaseModel):
    summary: str
    entities: List[EntityItem]
    keywords: List[str]