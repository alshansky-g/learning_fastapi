from contextlib import asynccontextmanager
from typing import Annotated

import redis.asyncio as redis
import uvicorn
from db import get_user_from_db, save_user_to_db
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from models import User
from security import auth_user, check_access_token, check_refresh_token
from services import hash_password, set_tokens


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(
        "redis://localhost:6379", encoding="utf-8"
        )
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)


@app.post("/register",
          dependencies=[Depends(RateLimiter(times=100, seconds=60))]
          )
async def register(user_data: User):
    user = get_user_from_db(user_data.username)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists")
    hashed_password = hash_password(user_data.password)
    save_user_to_db(user_data.username, hashed_password)
    return JSONResponse(status_code=201,
                        content={"message": "New user created"})


@app.post("/login",
          dependencies=[Depends(RateLimiter(times=500, seconds=60))])
async def login(user: Annotated[User, Depends(auth_user)],
                response: Response):
    set_tokens(response, user.username)
    return {"message": f"You logged in, {user.username}"}


@app.get("/profile")
async def get_profile(
    username: Annotated[str | None, Depends(check_access_token)],
):
    return {"message": f"Your profile page, {username}"}


@app.post("/refresh")
async def refresh(username: Annotated[str, Depends(check_refresh_token)]):
    return {"message": f"Your tokens have been refreshed, {username}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
