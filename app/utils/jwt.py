
import os
from datetime import datetime, timezone, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.configs import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes= Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm = Config.ALGORITHM)
    return encoded_jwt

