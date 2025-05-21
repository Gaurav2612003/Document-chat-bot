from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OCR_LANG: str = "eng"
    VECTOR_DB_DIR: str = "vector_db/"
    CHROMA_COLLECTION: str = "documents"
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    persist_directory: str = "vector_db/"
    is_persistent: bool = True  # Add this field
    chroma_api_impl: str = "duckdb"  # Add this field for the Chroma API implementation

# Instantiate the settings
settings = Settings()

