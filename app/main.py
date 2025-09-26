from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, analyze

app = FastAPI(title="Document Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="", tags=["upload"])
app.include_router(analyze.router, prefix="", tags=["analyze"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Document Analyzer API is running"}
