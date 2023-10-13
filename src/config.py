from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    app_title: str = "Simbir.GO API"
    app_description: str = "Api for an rent machines."
    app_version: str = "1.0.0"
    secret_key: str
    algorithm: str
    database_url: PostgresDsn


settings = Settings(_env_file="prod.env", _env_file_encoding="utf-8")
