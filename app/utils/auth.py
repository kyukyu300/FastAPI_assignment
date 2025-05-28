
from typing import Annotated

import jwt
from fastapi.params import Depends
from fastapi import HTTPException, status
from jwt import InvalidTokenError
from passlib.context import CryptContext

from app.configs import Config
from app.models.users import User
from app.utils.jwt import oauth2_scheme

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        credentials_exception.detail = "Invalid Token"
        raise credentials_exception
    user = User.get(id=user_id)
    if user is None:
        credentials_exception.detail = "User Not Found"
        raise credentials_exception
    return user


@staticmethod
def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

@staticmethod
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@classmethod
def authenticate(cls, username: str, password: str) -> User | None:
    for user in cls._data:
        if user.username == username and cls.verify_password(password, user.password):
            return user
    return None