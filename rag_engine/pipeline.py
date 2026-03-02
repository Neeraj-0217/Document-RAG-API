from rag_engine.loader import DocumentLoader
from rag_engine.chunker import TextChunker
from rag_engine.vector_store import VectorStore
from rag_engine.retriever import Retriever
from rag_engine.generator import ResponseGenerator

class RAGPipeline:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.vector_store = VectorStore(collection_name=session_id)
        self.retriever = Retriever(self.vector_store)
        self.generator = ResponseGenerator()
        self.chat_history = []

    def ingest(self, file_path:str) -> None:
        documents = self.loader.load(file_path)
        chunks = self.chunker.split(documents)

        self.vector_store.add_documents(chunks)

    def query(self, question: str) -> str:
        retrieved_docs = self.retriever.retrieve(question)
        answer = self.generator.generate(
            question=question,
            documents=retrieved_docs,
            history=self.chat_history
        )

        self.chat_history.append({
            'question': question,
            'answer': answer
        })

        if len(self.chat_history) > 5:
            self.chat_history.pop(0)
            
        return answer