from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List
from rag_engine import config
class DocumentLoader:
    def load(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load()