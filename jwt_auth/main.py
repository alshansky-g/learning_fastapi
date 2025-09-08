from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from models import User
from security import auth_user, check_token

app = FastAPI()


@app.post("/login")
async def login(user: Annotated[User, Depends(auth_user)]):
    return {"message": "You logged in"}


@app.get("/profile")
async def get_profile(
    username: Annotated[str | None, Depends(check_token)],
):
    return {"message": f"Your profile page, {username}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
