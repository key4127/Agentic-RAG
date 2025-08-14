from backend.routers import router

@router.get("/query", tags=["query"])
async def query(query: str):
    """
    Process a query and return results.
    """
    return {"query": query, "result": "This is a placeholder result."}