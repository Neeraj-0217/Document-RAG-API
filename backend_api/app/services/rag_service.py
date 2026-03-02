from rag_engine.pipeline import RAGPipeline


class RAGService:
    def __init__(self):
        # Dictionary to hold pipelines for each session
        self.active_sessions = {}

    def get_pipeline(self, session_id: str) -> RAGPipeline:
        if session_id not in self.active_sessions:
            # Initialize a new pipeline for the new session
            self.active_sessions[session_id] = RAGPipeline(session_id=session_id)
        return self.active_sessions[session_id]

    def ingest(self, session_id: str, file_path: str):
        pipeline = self.get_pipeline(session_id)
        pipeline.ingest(file_path)

    def query(self, session_id: str, query: str) -> str:
        pipeline = self.get_pipeline(session_id)
        return pipeline.query(query)