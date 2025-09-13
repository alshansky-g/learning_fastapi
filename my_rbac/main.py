from typing import Annotated

import uvicorn
from database import get_user
from fastapi import Depends, FastAPI
from models import User
from rbac import Permission, Role

app = FastAPI()


@app.get("/protected")
async def get_protected_resource(
    user: Annotated[User, Depends(Permission(required=Role.ADMIN))]
):
    return {"message": f"Welcome, {user.username}"}


@app.get("/profile")
async def get_profile(
    user: Annotated[User, Depends(Permission(required=Role.USER))]
):
    return {"message": f"Welcome to your profile page, {user.username}"}


@app.get("/")
async def main_page(
    user: Annotated[User, Depends(get_user)] = User()
):
    return {"message": f"Welcome, {user.username}"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
