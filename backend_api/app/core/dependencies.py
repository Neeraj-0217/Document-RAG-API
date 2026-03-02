from fastapi import Request

def get_rag_service():
    # Provide the globally initialized component without rebuilding it
    from backend_api.app.main import rag_service_instance
    return rag_service_instance
