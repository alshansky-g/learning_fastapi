from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from config import config
from db import get_user_from_db
from fastapi import Cookie, HTTPException, Response, status
from models import User
from services import check_hashes


def auth_user(credentials: User, response: Response):
    user = get_user_from_db(credentials.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    passwords_match = check_hashes(
         credentials.password, user["password"]
    )
    if not passwords_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization failed")
    token = create_jwt_token({"username": credentials.username})
    response.set_cookie(key="access_token",
                        value=token,
                        httponly=True, secure=True)
    return credentials


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
        payload = jwt.decode(jwt=access_token,
                        key=config.secret_key,
                        algorithms=[config.algorithm])
        return payload.get("username")
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Expired token") from err
    except jwt.InvalidSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token") from err
