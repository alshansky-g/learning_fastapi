from pydantic import BaseModel


class UserIn(BaseModel):
    username: str = "guest"


class User(UserIn):
    role: str = "guest"
