import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings as LlamaIndexSettings
from llama_index.llms.openai_like import OpenAILike
from backend.dependencies import get_query_engine
from backend.config import Settings
from backend.core.embedding.embedding_model import EmbeddingModel
from backend.core.storage.weaviate import WeaviateStorage

query = "I want to learn about CS, please give me some resources. Please answer in Chinese."

def query_engine_test(query: str) -> None:
    load_dotenv()

    settings = Settings()
    embedding_model = EmbeddingModel(settings.embedding_model)
    weaviate_storage = WeaviateStorage(
        settings.weaviate_db_name, 
        settings.embedding_model,
        settings.weaviate_host,
        settings.weaviate_port
    )

    LlamaIndexSettings.llm = OpenAILike(
        model="deepseek-chat",
        api_base="https://api.deepseek.com/beta",
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    LlamaIndexSettings.embed_model = embedding_model.get_embedding_model()

    query_engine = get_query_engine()

    print(f"query: {query}")
    print(query_engine.query(query))

    weaviate_storage.close()

query_engine_test(query)