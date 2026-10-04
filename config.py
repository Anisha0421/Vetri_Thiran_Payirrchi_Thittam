from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-this-secret-key"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    database_url: str = "sqlite:///./pocketsmart.db"

    frontend_origins: str = (
        "http://127.0.0.1:8000,http://localhost:8000"
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()