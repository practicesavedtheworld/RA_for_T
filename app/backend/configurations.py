from pathlib import Path
from typing import Self, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_URL: str | None = None

    TEST_DB_HOST: str
    TEST_DB_USER: str
    TEST_DB_PORT: int
    TEST_DB_PASSWORD: str
    TEST_DB_NAME: str
    TEST_DB_URL: str | None = None

    URL: str

    MODE: str = Literal["TEST", "PROD", "DEV"]
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
        db_driver_info = "postgresql+asyncpg://"
        db_params = f"{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}"
        test_db_params = f"{s.TEST_DB_USER}:{s.TEST_DB_PASSWORD}@{s.TEST_DB_HOST}:{s.TEST_DB_PORT}/{s.TEST_DB_NAME}"

        self.DB_URL = f"{db_driver_info}{db_params}"
        self.TEST_DB_URL = f"{db_driver_info}{test_db_params}"


settings = Settings()
