from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from passlib.context import CryptContext

class Settings(BaseSettings):
    weaviate_db_name: str = "Agentic_RAG_Docs"
    embedding_model: str = "local:BAAI/bge-m3"
    rerank_model: str = "ms-marco-TinyBERT-L-2-v2"
    rerank_node_num: int = 10
    weaviate_host: str = "localhost"
    weaviate_http_port: int = 8081
    weaviate_grpc_port: int = 50051
    jwt_secret_key: str = "ff99dc45a84bd00c01ca7e725fde36cfe403587772c1d9458a5a7dbfc2daf80e"
    pwd_context = CryptContext(schemes=["bycrpt"], deprecated="auto")
    jwt_hash_algorithm: str = "HS256"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )