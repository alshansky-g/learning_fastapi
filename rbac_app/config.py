from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 0

    model_config = SettingsConfigDict({"extra": "ignore",
                                       "env_file": ".env"})


config = Config()
