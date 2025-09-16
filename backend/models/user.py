from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str

class UserAuth(BaseModel):
    user_id: str
    password: str