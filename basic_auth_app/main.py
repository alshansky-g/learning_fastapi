from typing import Annotated

import uvicorn
from auth import User, authenticate_user
from db import save_user_to_db
from fastapi import Depends, FastAPI
from models import UserBase
from services import hash_password

app = FastAPI()


@app.post("/register")
async def register_user(user: User):
    hashed_password = await hash_password(user.password)
    save_user_to_db(username=user.username,
                    hashed_password=hashed_password)
    return {"message": f"Welcome, {user.username}"}


@app.get("/login")
def login_user(
    user: Annotated[UserBase, Depends(authenticate_user)]
    ):
    return {"message": f"Welcome, {user.username}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
