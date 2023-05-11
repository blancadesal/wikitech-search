import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import models, ping, search
from app.api.processing import load_similarity_index

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ping.router)
    app.include_router(search.router)
    app.include_router(models.router)

    return app


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    log.info("Loading similarity index...")
    await load_similarity_index()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
