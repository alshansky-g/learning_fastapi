from typing import Annotated

from db import get_user_from_db
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User
from services import verify_password

security = HTTPBasic()


async def authenticate_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
        ):
    user = get_user_from_db(User(username=credentials.username,
                                 password=credentials.password))
    if user:
        passwords_match = await verify_password(
            password=credentials.password,
            hashed_password=user.hashed_password)
        if passwords_match:
            return user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"})
