from fastapi import Depends
from llama_index.core.query_engine import BaseQueryEngine

async def query(query: str, query_engine: BaseQueryEngine):
    print(query)
    response = query_engine.query(query)
    return {
       "query": query,
       "answer": str(response)
    }