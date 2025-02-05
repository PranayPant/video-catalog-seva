import os
import requests

from ..decorators import handle_exceptions
from ..custom_types import TranscriptSentence


@handle_exceptions
def get_sentences_from_transcript(transcript_id: str) -> list[TranscriptSentence]:
    """Get sentences from an AssemblyAI transcript."""

    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}/sentences"
    headers = {
        "authorization": os.getenv("ASSEMBLYAI_API_KEY") or "",
    }
    response = requests.get(url, headers=headers, timeout=10)
    sentences = response.json().get("sentences", [])

    return [
        TranscriptSentence(
            text=sentence["text"],
            start=int(sentence["start"]),
            end=int(sentence["end"]),
        )
        for sentence in sentences
    ]
