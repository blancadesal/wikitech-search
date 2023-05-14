import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import models, ping, search
from app.processing import load_similarity_index

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    app = FastAPI()
    api_router = APIRouter()

    origins = [
        "https://wikitech-search.toolforge.org",
        "http://localhost",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_router.include_router(ping.router)
    api_router.include_router(search.router)
    api_router.include_router(models.router)

    app.include_router(api_router, prefix="/api")

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
