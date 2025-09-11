from typing import Annotated

from database import get_user
from fastapi import Depends, HTTPException, status
from models import User

ROLE_PERMISSIONS = {
    "admin": {"create", "read", "update", "delete"},
    "user": {"read", "update"},
    "guest": {"read"}
}


class PermissionChecker:
    def __init__(self, required: set[str]) -> None:
        self.required = required

    async def __call__(
            self, user: Annotated[User, Depends(get_user)]
            ) -> User:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден")
        permissions = ROLE_PERMISSIONS.get(user.role, set())
        if not self.required.issubset(permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для доступа",
            )
        return user
