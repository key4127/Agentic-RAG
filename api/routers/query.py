from fastapi import APIRouter, Depends
from api.services.agent.course_agent import CourseAgent
from api.services.query_service import query as query_service
from api.dependencies import get_agent

router = APIRouter()

@router.get("/query/{query}", tags=["query"])
async def query(query: str, agent: CourseAgent = Depends(get_agent)):
    response = await query_service(query, agent)
    return {"response": response}