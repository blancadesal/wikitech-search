from fastapi import APIRouter

from app.api.schemas import QuerySchema, ResultSchema
from app.processing import get_answer, get_inputs

router = APIRouter()


@router.get("/search", response_model=ResultSchema)
def search(query: str):
    inputs = get_inputs(query, result_depth=3)
    answer = get_answer(query, [i["text"] for i in inputs])
    result = ResultSchema(
        query=query, search_results=inputs, answer=answer
    )
    return result
