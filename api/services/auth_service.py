import jwt
import bcrypt
from typing import Optional
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from api.mysql import SessionDep
from api.config import Settings
from api.models import UserAuth
from api.auth import Token, TokenData
from api.services.user_service import get_user_by_name, create_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_id(token = Depends(oauth2_scheme)) -> str:
    settings = Settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_hash_algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user_by_name(token_data.username)
    return user.id


async def register(name: str, password: str, session: SessionDep) -> bool:
    if get_user_by_name(name, session) is not None:
        return False
    user = create_user(name, session)
    create_auth(user.id, password, session)
    return True


async def login(name: str, password: str, session: SessionDep):
    fail_result = {
        "result": "fail",
        "error": "wrong username or password"
    }
    success_result = {
        "result": "success"
    }

    user = get_user_by_name(name, session)
    
    if user is None:
        return fail_result
    
    auth = get_auth_by_id(user.id, session)

    if auth is None:
        return fail_result
    
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        auth.password.encode("utf-8")
    ):
        return fail_result
    else:
        return success_result


async def logout():
    pass


def get_auth_by_id(id: str, session: SessionDep) -> Optional[UserAuth]:
    auth = session.get(UserAuth, id)
    return auth


def create_auth(id: str, password: str, session: SessionDep):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    hashed_pw = hashed.decode("utf-8")

    userAuth = UserAuth()
    userAuth.user_id = id
    userAuth.password = hashed_pw

    session.add(userAuth)
    session.commit()
    session.refresh(userAuth)

    return userAuth