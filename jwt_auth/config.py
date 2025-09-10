from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    algorithm: str = ""
    secret_key: str = ""
    refresh_token_ttl: int = 0
    access_token_ttl: int = 0

    model_config = SettingsConfigDict({"env_file": ".env",
                                       "extra": "ignore"})


config = Config()
