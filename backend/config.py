from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    weaviate_db_name: str = "Agentic_RAG_Docs"
    embedding_model: str = "local:BAAI/bge-m3"
    weaviate_host: str = "localhost"
    weaviate_port: int = 8081

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"