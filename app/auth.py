import time
import uuid

from environs import Env
from fastapi import Cookie, FastAPI
from fastapi.responses import JSONResponse
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import BaseModel

env = Env()
env.read_env()
SECRET_KEY = env.str("SECRET_KEY")
MAX_AGE = env.int("MAX_AGE")

s = URLSafeTimedSerializer(SECRET_KEY)

app = FastAPI()


class User(BaseModel):
    login: str
    password: str


db_users = [
    {"login": "Vasily007", "password": '123456'},
    {"login": "Olga2001", "password": "01012001"}
]


@app.post("/login")
async def login(user_data: User):
    for user in db_users:
        if (user['login'] == user_data.login and
            user['password'] == user_data.password):
            token = s.dumps({"uuid": str(uuid.uuid4()),
                            "last_active": int(time.time()),
                            "login": user_data.login
                            })
            response = JSONResponse({"message": "You logged in successfully."})
            response.set_cookie(key="session_token", value=token,
                                httponly=True, secure=True, max_age=MAX_AGE)
            return response
    return {"message": "no user found"}


@app.get("/user")
async def get_user(session_token: str = Cookie(default=None)):
    try:
        session_cookie = s.loads(session_token, max_age=MAX_AGE)
        response = JSONResponse(
                content={
                    "message": f"Your profile data, {session_cookie["login"]}"
                    })
        if 10 <= time.time() - session_cookie["last_active"] <= 15:
            token = s.dumps({"login": session_cookie["login"],
                             "uuid": session_cookie["uuid"],
                             "last_active": int(time.time())})
            response.set_cookie(key="session_token", value=token,
                                httponly=True, secure=True, max_age=MAX_AGE)
        print(time.time() - session_cookie["last_active"])
        return response
    except (SignatureExpired, TypeError):
        return JSONResponse({"message": "Session expired"},
                            status_code=401)
    except BadSignature:
        return JSONResponse({"message": "Invalid session"},
                             status_code=401)
