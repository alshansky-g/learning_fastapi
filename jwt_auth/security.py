from typing import Annotated

import jwt
from config import config
from db import get_token_from_db, get_user_from_db
from fastapi import Cookie, HTTPException, Response, status
from models import User
from services import passwords_match, set_tokens


def auth_user(credentials: User):
    user = get_user_from_db(credentials.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if not passwords_match(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization failed")
    return credentials


def check_access_token(access_token: Annotated[str | None, Cookie()] = None):
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
    except (jwt.InvalidSignatureError, jwt.DecodeError) as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token") from err


def check_refresh_token(refresh_token: Annotated[str, Cookie()],
                        response: Response):
    try:
        payload = jwt.decode(jwt=refresh_token,
                             key=config.secret_key,
                             algorithms=[config.algorithm])
        username = payload.get("username")
        token_in_db = get_token_from_db(username)
        if not token_in_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token")
        set_tokens(response, username)
        return username
    except (jwt.ExpiredSignatureError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expired") from None
