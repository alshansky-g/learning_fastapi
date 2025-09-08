from typing import Annotated

import uvicorn
from db import get_user_from_db, save_user_to_db
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import User
from security import auth_user, check_token
from services import hash_password

app = FastAPI()


@app.post("/register")
async def register(user_data: User):
    user = get_user_from_db(user_data.username)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")
    hashed_password = hash_password(user_data.password)
    save_user_to_db(user_data.username, hashed_password)
    return JSONResponse(status_code=201,
                        content={"message": "New user created"})


@app.post("/login")
async def login(user: Annotated[User, Depends(auth_user)]):
    return {"message": f"You logged in, {user.username}"}


@app.get("/profile")
async def get_profile(
    username: Annotated[str | None, Depends(check_token)],
):
    return {"message": f"Your profile page, {username}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
