from fastapi import APIRouter, Response, status
from api.mysql import SessionDep
from api.services.auth_service import register as register_service

router = APIRouter()

@router.post("/auth/register", tags=["register"])
async def register(name: str, password: str, response: Response, session: SessionDep):
    result = await register_service(name, password, session)
    if result:
        response.status_code = status.HTTP_201_CREATED
        return {"result": "success"}
    else:
        response.status_code = status.HTTP_403_UNAUTHORIZED
        return {"result": "fail"}