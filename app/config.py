import logging
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "prod"
    testing: bool = bool(0)
    emb_dir: Path = Path("/code/embeddings")
    custom_ua: str | None = None


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()
