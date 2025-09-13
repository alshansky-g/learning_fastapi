from dataclasses import dataclass
from typing import Annotated

from database import get_user
from fastapi import Depends, HTTPException, status
from models import User


@dataclass
class Role:
    ADMIN = {"create", "read", "update", "delete"}
    USER = {"read", "update"}
    GUEST = {"read"}

    @classmethod
    def get(cls, role: str) -> set:
        return getattr(cls, role.upper())


class Permission:
    def __init__(self, required: set[str]) -> None:
        self.required = required

    async def __call__(
            self, user: Annotated[User, Depends(get_user)]
            ) -> User:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден")
        permissions: set = Role.get(user.role)
        if not self.required.issubset(permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для доступа",
            )
        return user
