import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from app.config import get_settings, get_tortoise_config

log = logging.getLogger("uvicorn")


settings = get_settings()
TORTOISE_ORM = get_tortoise_config(settings)


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())