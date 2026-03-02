from pathlib import Path

# Model Settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHAT_MODEL = "llama3.2:1b"

# Paths
DATA_DIR = Path(__file__).parent / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_DB_PATH = DATA_DIR / "vector_db"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)


# Chunking Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Settings
TOP_K = 3
SIMILARITY_THRESHOLD = 0.0
MAX_K = 10

# Generation Settings
TEMPERATURE = 0.2
MAX_TOKENS = 512
