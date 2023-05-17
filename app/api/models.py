from fastapi import APIRouter, Depends

from app.model_manager import ModelManager, get_model_manager

router = APIRouter()


@router.get("/models", response_model=dict)
async def get_models(model_manager: ModelManager = Depends(get_model_manager)):
    """Get info about the models used for the API."""
    model_info = model_manager.get_model_info()
    return {"models": model_info}
