import logging
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "prod"
    testing: bool = bool(0)
    database_url: str = "sqlite:///data/project/fastapi-blueprint/db.sqlite3"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


def get_tortoise_config(settings: Settings):
    return {
        "connections": {"default": settings.database_url},
        "apps": {
            "models": {
                "models": ["app.models.tortoise", "aerich.models"],
                "default_connection": "default",
            },
        },
    }