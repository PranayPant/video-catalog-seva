from pydantic import BaseModel


class SearchMediaQuery(BaseModel):
    search_term: str
    google_drive_file_url: str | None = None
    fail_if_no_transcript: bool | None = None
    transcript_id: str | None = None


class SearchMediaLocation(BaseModel):
    start: int
    end: int
    relevance: float
    search_term: str


class SearchMediaResponse(BaseModel):
    locations: list[SearchMediaLocation]


class TranscriptSentence(BaseModel):
    text: str
    start: int
    end: int
