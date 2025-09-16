import os
from dotenv import load_dotenv
from llama_index.core import Settings as LlamaIndexSettings
from llama_index.llms.deepseek import DeepSeek
from api.dependencies import get_query_engine
from api.dependencies import get_embedding_model
from api.config import Settings

query = "I want to learn about CS, please give me some resources. Please answer in Chinese."

def query_engine_test(query: str) -> None:
    load_dotenv()

    LlamaIndexSettings.llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
    LlamaIndexSettings.embed_model = get_embedding_model()

    query_engine = get_query_engine()

    print(f"query: {query}")
    print(query_engine.query(query))

query_engine_test(query)