from typing import Annotated

from fastapi import Header
from pydantic import BaseModel, field_validator

MINIMUM_APP_VERSION = "0.0.2"


class CommonHeaders(BaseModel):
    user_agent: Annotated[str, Header()]
    accept_language: Annotated[str, Header()]
    x_current_version: Annotated[str, Header()]

    @field_validator("x_current_version")
    def version_check(cls, version: str):
        if len(chars := version.split(".")) != 3 or not all(
            c.isdigit() for c in chars
        ):
            raise ValueError("Неверный формат версии")
        if version < MINIMUM_APP_VERSION:
            raise ValueError("Требуется обновить приложение")
