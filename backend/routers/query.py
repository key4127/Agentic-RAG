from fastapi import APIRouter, Depends
from backend.core.agent.course_agent import CourseAgent
from backend.services.query_service import query as query_service
from backend.dependencies import get_agent

router = APIRouter()

@router.get("/query/{query}", tags=["query"])
async def query(query: str, agent: CourseAgent = Depends(get_agent)):
    response = await query_service(query, agent)
    return {"response": response}