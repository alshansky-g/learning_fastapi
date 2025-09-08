from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from config import config
from db import USERS_DB
from fastapi import Cookie, HTTPException, Response, status
from models import User


def auth_user(credentials: User, response: Response):
    for user in USERS_DB:
        if (user["username"] == credentials.username and
            user["password"] == credentials.password):
            token = create_jwt_token({"username": credentials.username})
            response.set_cookie(key="access_token",
                                value=token,
                                httponly=True, secure=True)
            return credentials
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials")


def create_jwt_token(user: dict):
    user.update({"exp": datetime.now(UTC) + timedelta(minutes=30)})
    token = jwt.encode(key=config.secret_key,
                       algorithm=config.algorithm,
                       payload=user)
    return token


def check_token(access_token: Annotated[str | None, Cookie()] = None):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(jwt=str(access_token),
                        key=config.secret_key,
                        algorithms=[config.algorithm])
        return payload.get("username")
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Expired token") from err
    except jwt.InvalidSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token") from err
