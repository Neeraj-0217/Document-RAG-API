from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend_api.app.api import routes_upload, routes_query
from backend_api.app.core.logger import logger
from backend_api.app.services.rag_service import RAGService

# Global service instance to be loaded on startup
rag_service_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the RAG service and models before taking requests
    logger.info("Starting up RAG application, initializing models...")
    global rag_service_instance
    rag_service_instance = RAGService()
    yield
    # Shutdown logic if necessary
    logger.info("Shutting down RAG application...")

app = FastAPI(title="RAG API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_upload.router)
app.include_router(routes_query.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Pass through standard HTTP Exceptions to FastAPI
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Catch-all for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled system error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_api.app.main:app", host="0.0.0.0", port=8000, reload=True)