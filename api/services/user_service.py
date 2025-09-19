import uuid
from typing import Optional
from sqlmodel import select
from api.mysql import SessionDep
from api.models import User


def get_user_by_id(id: str, session: SessionDep) -> Optional[User]:
    user = session.get(User, id)
    return user


def get_user_by_name(name: str, session: SessionDep) -> Optional[User]:
    statement = select(User).where(User.name == name)
    user = session.exec(statement=statement).first()
    return user


def create_user(name: str, session: SessionDep) -> Optional[User]:
    if get_user_by_name(name, session) is not None:
        return None
    
    id = uuid.uuid4()
    user = User()
    user.id = str(id)
    user.name = name

    session.add(user)
    session.commit()
    session.refresh(user)

    return user