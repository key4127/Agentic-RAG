import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from llama_index.core import Settings as LlamaIndexSettings
from llama_index.llms.deepseek import DeepSeek
from api.config import Settings
from llama_index.core.embeddings import resolve_embed_model
from api.routers.query import router as query_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    embedding_model = resolve_embed_model(settings.embedding_model)
    LlamaIndexSettings.llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
    LlamaIndexSettings.embed_model = embedding_model.get_embedding_model()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(query_router, prefix="")    

@app.get("/")
async def root():
    return {"message": "Hello World"}