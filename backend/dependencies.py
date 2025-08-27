from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core import VectorStoreIndex
from .core.embedding.embedding_model import EmbeddingModel
from .core.storage.weaviate import WeaviateStorage
from .config import Settings

vector_store_instance = None
global_query_engine = None
global_retriever = None

def get_vector_store_client() -> WeaviateStorage:
    global vector_store_instance
    if vector_store_instance is None:
        settings = Settings()
        vector_store_instance = WeaviateStorage(
            name=settings.weaviate_db_name, 
            model=settings.embedding_model, 
            host=settings.weaviate_host, 
            http_port=settings.weaviate_http_port,
            grpc_port=settings.weaviate_grpc_port
        )
    return vector_store_instance

def get_query_engine() -> BaseQueryEngine:
    global global_query_engine
    if global_query_engine is None:
        weaviate_storage = get_vector_store_client()
        vector_store = weaviate_storage.get_vector_store()
        global_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        global_query_engine = global_index.as_query_engine()
    return global_query_engine

def get_retriever() -> BaseRetriever:
    global global_retriever
    if global_retriever is None:
        weaviate_storage = get_vector_store_client()
        vector_store = weaviate_storage.get_vector_store()
        global_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        global_retriever = global_index.as_retriever()
    return global_retriever

def close_all() -> None:
    pass