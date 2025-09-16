import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from api.config import Settings

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class JWTUtil:

    def __init__(self):
        settings = Settings()
        self.pwd_context = settings.pwd_context
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_hash_algorithm

    def verify_password(self, plain, hash):
        return self.pwd_context.verify(plain, hash)
    
    def get_hash_password(self, pwd):
        return self.pwd_context.hash(pwd)
    
    def create_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt

