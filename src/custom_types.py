from pydantic import BaseModel

class SearchMediaQuery(BaseModel):
    search_term: str


class SearchMediaLocation(BaseModel):
    start_time: int
    end_time: int
    relevance: float

class SearchMediaResponse(BaseModel):
    locations: list[SearchMediaLocation]
