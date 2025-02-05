from typing import Annotated

from fastapi import FastAPI, APIRouter, BackgroundTasks, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .utils import get_file_id_from_url
from .api.google_drive import get_file_info

from .custom_types import SearchMediaQuery, SearchMediaResponse

app = FastAPI()
router = APIRouter(redirect_slashes=False)


@router.get("/api/v1/search")
def search_media(query: Annotated[SearchMediaQuery, Query()]) -> dict:
    response = query.model_dump()

    transcript_id = query.transcript_id
    if not transcript_id:
        file_id = get_file_id_from_url(query.google_drive_file_url)
        transcript_id = (get_file_info(file_id).get("properties") or {}).get(
            "transcript_id"
        )

    if not transcript_id:
        raise HTTPException(
            status_code=400,
            detail="No transcript associated with the file. Please create an AssemblyAI transcript first.",
        )

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
