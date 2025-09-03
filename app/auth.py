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
            token = s.dumps({"token": str(uuid.uuid4()),
                            "login": user_data.login
                            })
            response = JSONResponse({"message": "You logged in successfully."})
            response.set_cookie(key="session_token", value=token,
                                httponly=True, secure=True)
            return response
    return {"message": "no user found"}


@app.get("/user")
async def get_user(session_token: str = Cookie(default=None)):
    try:
        user_data = s.loads(session_token, max_age=MAX_AGE)
        return {"message": f"Your profile data, {user_data['login']}"}
    except SignatureExpired:
        return JSONResponse({"message": "Ваш токен просрочен"},
                            status_code=401)
    except BadSignature:
        return JSONResponse({"message": "Ваш токен повреждён или подделан"},
                        status_code=401)
