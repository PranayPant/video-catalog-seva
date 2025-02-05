from typing import Annotated

from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .api.assembly_ai import get_sentences_from_transcript

from .llm.gemini import GenAI
from .utils import get_file_id_from_url
from .api.google_drive import get_file_info
from .custom_types import SearchMediaQuery, SearchMediaResponse

app = FastAPI()
router = APIRouter(redirect_slashes=False)


@router.get("/api/v1/search")
def search_media(
    query: Annotated[SearchMediaQuery, Query()]
) -> SearchMediaResponse | None:
    """Search for text in a media file."""

    transcript_id = query.transcript_id
    if not transcript_id and query.google_drive_file_url:
        file_id = get_file_id_from_url(query.google_drive_file_url)
        transcript_id = (get_file_info(file_id).get("properties") or {}).get(
            "transcript_id"
        )

    if not transcript_id:
        raise HTTPException(
            status_code=400,
            detail="No transcript associated with the file. Please create an AssemblyAI transcript first.",
        )

    try:
        hindi_sentences = get_sentences_from_transcript(transcript_id)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error getting sentences from transcript. Please choose a different transcript or try again later.",
        ) from exc

    genai = GenAI()

    try:
        translated_sentences = genai.translate_sentences(hindi_sentences)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error translating sentences. Please try again later.",
        ) from exc

    try:
        locations = genai.locate_text_in_sentences(
            translated_sentences, query.search_term
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error locating text in sentences. Please try again later.",
        ) from exc

    response = SearchMediaResponse(locations=locations)

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
