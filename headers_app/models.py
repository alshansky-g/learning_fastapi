from typing import Annotated

from fastapi import Header
from pydantic import BaseModel


class CommonHeaders(BaseModel):
    user_agent: Annotated[str, Header()]
    accept_language: Annotated[str, Header()]
