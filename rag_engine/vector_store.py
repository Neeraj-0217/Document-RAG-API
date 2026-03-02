from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from rag_engine import config

# Initialize the heavy embedding model strictly ONCE at the module level
# This saves significant memory and CPU time and provides consistent performance for all sessions
GLOBAL_EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'}
)

class VectorStore:
    def __init__(self, collection_name: str):
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=GLOBAL_EMBEDDING_MODEL,
            persist_directory=str(config.VECTOR_DB_PATH)
        )

    def add_documents(self, documents: List[Document]) -> None:
        if not documents:
            raise ValueError("No documents provided for adding to vector store.")
        
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = config.TOP_K) -> List[Document]:
        if not query.strip():
            raise ValueError("No query provided for similarity search.")
        
        return self.vector_store.similarity_search(query, k=k)