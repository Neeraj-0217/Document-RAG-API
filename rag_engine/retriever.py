from typing import List
from langchain_core.documents import Document
from rag_engine.vector_store import VectorStore
from rag_engine import config

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = config.TOP_K) -> List[Document]:
        if not query.strip():
            raise ValueError("No query provided for retrieval.")
        
        return self.vector_store.similarity_search(query, k=k)