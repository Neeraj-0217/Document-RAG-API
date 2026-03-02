from pydantic import BaseModel

class QueryRequest(BaseModel):
    session_id: str
    query: str

class QueryResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    message: str
    session_id: str

    