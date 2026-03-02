from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend_api.app.services.rag_service import RAGService
from backend_api.app.schemas.rag_schema import UploadResponse
from backend_api.app.core.dependencies import get_rag_service
from backend_api.app.core.logger import logger

import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 1024 * 1024 * 10 # 10MB

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    rag_service: RAGService = Depends(get_rag_service)
):
    if not file.filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size allowed is 10MB.")

    try:
        file_path = UPLOAD_DIR / file.filename

        # Write file async in chunks to prevent blocking event loop
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024) # 1MB chunk size
                if not chunk:
                    break
                buffer.write(chunk)

        # In a very high traffic app, this processing should ideally be sent to a Celery worker.
        # But this suffices for an internal utility API.
        session_id = str(uuid.uuid4())
        rag_service.ingest(session_id=session_id, file_path=str(file_path))

        return {
            "message": "File uploaded and indexed successfully.",
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))