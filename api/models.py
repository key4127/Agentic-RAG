from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True)
    name: str = Field(default=None)


class UserAuth(SQLModel, table=True):
    __tablename__ = "user_auth"

    user_id: str = Field(default=None, primary_key=True)
    password: str = Field(default=None)