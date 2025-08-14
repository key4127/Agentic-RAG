from fastapi import FastAPI
from .routers.query import router as query_router

app = FastAPI()
app.include_router(query_router, prefix="")

@app.get("/")
async def root():
    return {"message": "Hello World"}