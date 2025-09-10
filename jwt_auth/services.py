from datetime import UTC, datetime, timedelta

import jwt
from config import config
from db import save_token_to_db
from fastapi import Response
from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    hashed_password = ctx.hash(password)
    return hashed_password


def passwords_match(password_in: str, hashed_password):
    return ctx.verify(password_in, hashed_password)


def create_token(user: dict, token_type: str, ttl: int):
    payload = user.copy()
    payload.update({"exp": datetime.now(UTC) + timedelta(
        seconds=ttl),
                    "type": token_type})
    access_token = jwt.encode(key=config.secret_key,
                              algorithm=config.algorithm,
                              payload=payload)
    return access_token


def set_tokens(response: Response, username: str):
    access_token = create_token(
        {"username": username}, token_type="access",
        ttl=config.access_token_ttl)
    response.set_cookie(key="access_token",
                        value=access_token,
                        httponly=True, secure=True)
    refresh_token = create_token(
        {"username": username}, token_type="refresh",
        ttl=config.refresh_token_ttl)
    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True, secure=True, path="/refresh")
    save_token_to_db(username, refresh_token)
