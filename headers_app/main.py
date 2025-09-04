from datetime import UTC, datetime
from typing import Annotated

from fastapi import FastAPI, Header

from .models import CommonHeaders

app = FastAPI()


@app.get("/headers")
async def get_headers(headers: Annotated[CommonHeaders, Header()]):
    # if not user_agent or not accept_language:
    #     return HTTPException(status_code=400,
    #                          detail="Expected Accept-Language and User-Agent headers")
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language,
    }


@app.get("/info")
async def get_info(headers: Annotated[CommonHeaders, Header()]):
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language,
            "X-Server-Time": datetime.now(UTC).isoformat(timespec="seconds")
        }
    }
