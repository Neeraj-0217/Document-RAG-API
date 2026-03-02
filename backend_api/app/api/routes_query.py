from fastapi import APIRouter, Depends, HTTPException
from backend_api.app.services.rag_service import RAGService
from backend_api.app.schemas.rag_schema import QueryRequest, QueryResponse
from backend_api.app.core.dependencies import get_rag_service
from backend_api.app.core.logger import logger

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    try:
        logger.info(f"Processing query for session_id: {request.session_id}")

        response = rag_service.query(
            session_id=request.session_id,
            query=request.query
        )
        return {"answer": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
