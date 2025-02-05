from pydantic import BaseModel


class SearchMediaQuery(BaseModel):
    search_term: str
    google_drive_file_url: str
    fail_if_no_transcript: bool | None = None
    transcript_id: str | None = None


class SearchMediaLocation(BaseModel):
    start_time: int
    end_time: int
    relevance: float


class SearchMediaResponse(BaseModel):
    locations: list[SearchMediaLocation]
