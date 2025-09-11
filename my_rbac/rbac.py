from typing import Annotated

from database import get_user
from fastapi import Depends, HTTPException, status
from models import User


class PermissionChecker:
    def __init__(self, roles: list[str]) -> None:
        self.roles = roles

    async def __call__(self, user: Annotated[User, Depends(get_user)]) -> User:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден")
        if user.role not in self.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для доступа",
            )
        return user
