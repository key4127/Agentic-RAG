from fastapi import Depends
from llama_index.core import Settings as LlamaIndexSettings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.postprocessor.flashrank_rerank import FlashRankRerank
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core import get_response_synthesizer
from llama_index.core import VectorStoreIndex
from llama_index.core.embeddings import resolve_embed_model

from api.services.tool.vector_tool import VectorTool
from api.services.tool.web_tool import WebTool
from api.services.agent.course_agent import CourseAgent
from .weaviate import WeaviateStorage
from .config import Settings

embedding_model = None

vector_store_instance = None
global_query_engine = None
global_retriever = None
global_synthesizer = None
flash_reranker = None

vector_db_tool = None
web_tool = None
course_agent = None

def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        settings = Settings()
        embedding_model = resolve_embed_model(settings.embedding_model)
    return embedding_model

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

def get_query_engine() -> RetrieverQueryEngine:
    global global_query_engine
    if global_query_engine is None:
        weaviate_storage = get_vector_store_client()
        vector_store = weaviate_storage.get_vector_store()
        global_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        retriever = global_index.as_retriever()
        global_query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.95)],
        )
        #global_query_engine = global_index.as_query_engine()
    return global_query_engine

def get_retriever() -> BaseRetriever:
    global global_retriever
    if global_retriever is None:
        weaviate_storage = get_vector_store_client()
        vector_store = weaviate_storage.get_vector_store()
        global_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        global_retriever = global_index.as_retriever(similarity_top_k=7)
    return global_retriever

def get_synthesizer() -> BaseSynthesizer:
    global global_synthesizer
    if global_synthesizer is None:
        global_synthesizer = get_response_synthesizer(
            response_mode=ResponseMode.COMPACT
        )
    return global_synthesizer

def get_flash_reranker() -> FlashRankRerank:
    global flash_reranker
    if flash_reranker is None:
        settings = Settings()
        flash_reranker = FlashRankRerank(
            model=settings.rerank_model,
            top_n=settings.rerank_node_num
        )
    return flash_reranker

def get_vector_tool(
    retriever = Depends(get_retriever),
    reranker = Depends(get_flash_reranker),
    synthesizer = Depends(get_synthesizer)
) -> VectorTool:
    global vector_db_tool
    if vector_db_tool is None:
        vector_db_tool = VectorTool(retriever, reranker, synthesizer)
    return vector_db_tool

def get_web_tool() -> WebTool:
    global web_tool
    if web_tool is None:
        web_tool = WebTool()
    return web_tool

def get_agent(
    vector_tool: VectorTool = Depends(get_vector_tool),
    web_tool: WebTool = Depends(get_web_tool)
) -> CourseAgent:
    global course_agent
    if course_agent is None:
        course_agent = CourseAgent(vector_tool, web_tool)
    return course_agent

def close_all() -> None:
    pass