from fastapi import APIRouter

from app.processing import get_model_info

router = APIRouter()

MODEL_INFO = get_model_info()


@router.get("/models", response_model=dict)
async def get_models():
    """Get info about the models used for the API."""
    return {"models": MODEL_INFO}
