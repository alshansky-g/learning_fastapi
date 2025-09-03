import uuid

from environs import Env
from fastapi import Cookie, FastAPI, Response
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

# user_tokens = {}


@app.post("/login")
async def login(response: Response, user_data: User):
    for user in db_users:
        if (user['login'] == user_data.login and
            user['password'] == user_data.password):
            token = s.dumps({"token": str(uuid.uuid4()),
                            "login": user_data.login
                            })
            response.set_cookie(key="session_token", value=token,
                                httponly=True, secure=True)
            return {"message": "You logged in successfully."}
    return {"message": "no user found"}


@app.get("/user")
async def get_user(session_token: str = Cookie(default=None)):
    if session_token is None:
        return Response(status_code=401)
    try:
        user_data = s.loads(session_token, max_age=MAX_AGE)
        return {"message": f"Your profile data, {user_data['login']}"}
    except SignatureExpired:
        return JSONResponse({"message": "Ваш токен просрочен"},
                            status_code=401)
    except BadSignature:
        return JSONResponse({"message": "Ваш токен повреждён или подделан"},
                        status_code=401)
