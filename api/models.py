from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str = Field(default=None)


class UserAuth(SQLModel, table=True):
    user_id: str = Field(default=None, primary_key=True)
    password: str = Field(default=None)