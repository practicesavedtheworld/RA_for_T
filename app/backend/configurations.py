from pathlib import Path
from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_URL: str | None = None
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=[f"{BASE_DIR}/fake_env_file.txt", f"{BASE_DIR}/.env"]
    )

    def __init__(self: Self, **kwargs):
        """
        Creating a DB_URL attribute after initialization (after all
        the env-vars have been parsed, it will be initialized.)
        After the initialization method creates the DB_URL attribute."""

        s: Self = self
        super().__init__(**kwargs)
        self.DB_URL = f"postgresql+asyncpg://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"


settings = Settings()
