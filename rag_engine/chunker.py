from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rag_engine import config
from typing import List

class TextChunker:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

    def split(self, documents: List[Document]) -> List[Document]:
        if not documents:
            raise ValueError("No documents provided for splitting.")
        
        return self.text_splitter.split_documents(documents)