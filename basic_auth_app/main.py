from typing import Annotated

import uvicorn
from auth import authenticate_user
from db import save_user_to_db
from fastapi import Depends, FastAPI
from models import User, UserInDB
from services import hash_password

app = FastAPI()


@app.post("/register")
async def register_user(user: User):
    hashed_password = await hash_password(user.password)
    user_in_db = UserInDB(username=user.username,
                          hashed_password=hashed_password)
    save_user_to_db(user_in_db)
    return {"message": f"Welcome, {user.username}"}


@app.get("/login")
def login_user(
    user: Annotated[UserInDB, Depends(authenticate_user)]
    ):
    print(user, f"тип: {type(user)}")
    return {"message": f"Welcome, {user.username}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
