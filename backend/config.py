from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    weaviate_db_name: str = "Agentic_RAG_Docs"
    embedding_model: str = "local:BAAI/bge-m3"
    weaviate_host: str = "localhost"
    weaviate_http_port: int = 8081
    weaviate_grpc_port: int = 50051

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )