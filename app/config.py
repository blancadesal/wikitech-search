import logging
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "prod"
    testing: bool = bool(0)
    database_url: str = "sqlite://db.sqlite3"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
