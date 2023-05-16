from pydantic import BaseModel


class SearchSchema(BaseModel):
    title: str
    score: float
    text: str


class ResultSchema(BaseModel):
    query: str
    search_results: list[SearchSchema]
    answer: str | None
