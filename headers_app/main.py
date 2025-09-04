from datetime import UTC, datetime
from typing import Annotated

from fastapi import FastAPI, Header

from .models import CommonHeaders

app = FastAPI()


@app.get("/headers")
async def get_headers(headers: Annotated[CommonHeaders, Header()]):
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
            "X-Server-Time": datetime.now(UTC).isoformat(timespec="seconds"),
        },
    }
