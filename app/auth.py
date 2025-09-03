import uuid

from fastapi import Cookie, FastAPI, Response
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    password: str


user_tokens = {}


@app.post("/login")
async def login(response: Response, user: User):
    print(f"Получен юзер {user}")
    token = str(uuid.uuid4())
    response.set_cookie(key="session_token", value=token,
                        httponly=True, secure=True)
    user_tokens[token] = user
    return {"message": "valid login data"}


@app.get("/user")
async def get_user(session_token: str = Cookie(default=None)):
    if session_token in user_tokens:
        return {"message": f"Your profile data: {user_tokens[session_token]}"}
    return Response(status_code=401)
