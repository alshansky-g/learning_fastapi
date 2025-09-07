from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mode: str = ""
    docs_user: str = ""
    docs_password: str = ""
    openapi_url: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()
