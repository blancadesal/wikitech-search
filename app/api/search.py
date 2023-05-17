from fastapi import APIRouter, Depends

from app.api.schemas import ResultSchema
from app.model_manager import ModelManager, get_model_manager

router = APIRouter()


@router.get("/search", response_model=ResultSchema)
def search(query: str, model_manager: ModelManager = Depends(get_model_manager)):
    inputs = model_manager.get_inputs(query, result_depth=3)
    answer = model_manager.get_answer(query, [i["text"] for i in inputs])
    result = ResultSchema(query=query, search_results=inputs, answer=answer)
    return result
