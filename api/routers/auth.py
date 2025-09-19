from fastapi import APIRouter, Response, status
from api.mysql import SessionDep
from api.services.auth_service import register as register_service
from api.services.auth_service import login as login_service

router = APIRouter()

@router.post("/auth/register", tags=["register"])
async def register(name: str, password: str, response: Response, session: SessionDep):
    result = await register_service(name, password, session)
    if result:
        response.status_code = status.HTTP_201_CREATED
        return {"result": "success"}
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return {"result": "fail"}


@router.post("/auth/login", tags=["login"])
async def login(name: str, password: str, response: Response, session: SessionDep):
    result = await login_service(name, password, session)
    if result["result"] == "success":
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return result


@router.delete("/auth/logout", tags=["logout"])
async def logout(session: SessionDep):
    pass