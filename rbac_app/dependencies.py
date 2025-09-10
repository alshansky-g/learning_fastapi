from db import get_user
from fastapi import Depends, HTTPException, status
from models import User
from security import get_user_from_token


def get_current_user(
    current_username: str = Depends(get_user_from_token),
) -> User:
    user = get_user(current_username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user
