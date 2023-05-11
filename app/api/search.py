from fastapi import APIRouter

from app.api.processing import get_answer, get_inputs
from app.models.schemas import QuerySchema, ResultSchema

router = APIRouter()


@router.post("/search", response_model=ResultSchema)
def search(search_query: QuerySchema):
    inputs = get_inputs(search_query.query, result_depth=3)
    answer = get_answer(search_query.query, [i["text"] for i in inputs])
    result = ResultSchema(
        query=search_query.query, search_results=inputs, answer=answer
    )
    return result
