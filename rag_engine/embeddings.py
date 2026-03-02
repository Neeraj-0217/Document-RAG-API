from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from rag_engine import config

class EmbeddingModel:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )

    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        if not documents:
            raise ValueError("No documents provided for embedding.")
        
        texts = [doc.page_content for doc in documents]
        return self.embedding.embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
        if not query.strip():
            raise ValueError("No query provided for embedding.")
        
        return self.embedding.embed_query(query)

    
