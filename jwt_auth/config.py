from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    algorithm: str = ""
    secret_key: str = ""

    model_config = SettingsConfigDict({"env_file": ".env",
                                       "extra": "ignore"})


config = Config()
