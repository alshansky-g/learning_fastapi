from typing import Annotated

import uvicorn
from auth import authenticate_user, docs_auth
from config import config
from db import save_user_to_db
from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials
from schemas import User, UserInDB
from services import hash_password

if config.mode == "DEV":
    app = FastAPI(redoc_url=None, openapi_url=None)
    config.openapi_url = "/openapi.json"
    @app.get("/docs", include_in_schema=False)
    def get_docs(
        _: Annotated[HTTPBasicCredentials, Depends(docs_auth)]
        ):
        return get_swagger_ui_html(openapi_url=config.openapi_url,
                                title="Docs",
                                swagger_ui_parameters={
                                    "persistAuthorization": True
                                })

    @app.get("/openapi.json", include_in_schema=False)
    def get_docs_json(_: Annotated[HTTPBasicCredentials, Depends(docs_auth)]):
        return app.openapi()

elif config.mode == "PROD":
    app = FastAPI(openapi_url=None, redoc_url=None, docs_url=None)
else:
    raise ValueError("недопустимое значение переменной MODE")


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
