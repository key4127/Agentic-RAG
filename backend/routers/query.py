from fastapi import APIRouter, Depends
from llama_index.core.query_engine import BaseQueryEngine
from backend.services.query_service import query as query_service
from backend.dependencies import get_query_engine

router = APIRouter()

@router.get("/query/{query}", tags=["query"])
async def query(query: str, query_engine: BaseQueryEngine = Depends(get_query_engine)):
    response = await query_service(query, query_engine)
    return {"response": response}