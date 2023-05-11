from fastapi import APIRouter

from app.api.processing import get_model_info

router = APIRouter()

emb_model_name = "sentence-transformers/all-mpnet-base-v2"
qa_model_name = "deepset/tinyroberta-squad2"
MODEL_INFO = get_model_info()


@router.get("/models", response_model=dict)
async def get_models():
    """Get info about the models used for the API."""
    return {"models": MODEL_INFO}
