from pydantic import BaseModel, Field


class QuerySchema(BaseModel):
    query: str = Field(..., description="The query to search")


class SearchSchema(BaseModel):
    title: str
    score: float
    text: str


class ResultSchema(BaseModel):
    query: str
    search_results: list[SearchSchema]
    answer: str | None
