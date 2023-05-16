import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import models, ping, search
from app.model_manager import get_model_manager

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
    api_router.include_router(models.router)
    api_router.include_router(search.router)

    app.include_router(api_router, prefix="/api")

    return app

app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    log.info("Loading similarity index...")
    model_manager = get_model_manager()
    model_manager.load_similarity_index()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")

