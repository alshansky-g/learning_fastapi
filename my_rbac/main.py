from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from models import User
from rbac import PermissionChecker

app = FastAPI()


@app.get("/protected")
async def get_protected_resource(
    user: Annotated[User, Depends(PermissionChecker({"create", "delete"}))]
):
    return {"message": f"Welcome, {user.username}"}


@app.get("/profile")
async def get_profile(
    user: Annotated[User, Depends(PermissionChecker({"read", "update"}))]
):
    return {"message": f"Welcome to your profile page, {user.username}"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
