from typing import Annotated

from fastapi import FastAPI, APIRouter, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware

from .custom_types import SearchMediaQuery, SearchMediaResponse

app = FastAPI()
router = APIRouter(redirect_slashes=False)

@router.get("/api/v1/search")
def search_media(query: Annotated[SearchMediaQuery, Query()]) -> dict:
    response = query.model_dump()

    return response



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
