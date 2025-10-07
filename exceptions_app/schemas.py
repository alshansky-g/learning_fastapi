from pydantic import BaseModel


class ResponseErrorA(BaseModel):
    error_message: str


class ResponseErrorB(ResponseErrorA):
    pass
