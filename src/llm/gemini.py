import json
import google.generativeai as genai

from ..custom_types import (
    TranscriptSentence,
    SearchMediaLocation,
)
from ..utils import profile_execution_time


class GenAI:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
        )

    @profile_execution_time
    def translate_sentences(
        self, sentences: list[TranscriptSentence]
    ) -> list[TranscriptSentence]:

        hindi_sentences = [sentence.text for sentence in sentences]

        prompt = (
            """
            You are given a stringified array of sentences from a Hindi transcript.
            Translate the text from Hindi to English and return the modified array.

            Use this as input:
            sentences = """
            + str(hindi_sentences)
            + """
            """
        )
        response = self.model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[str]
            ),
        )
        translated_texts = json.loads(response.text)
        result = [
            TranscriptSentence(
                **sentence.model_dump(include={"start", "end"}),
                text=translated_text,
            )
            for sentence, translated_text in zip(sentences, translated_texts)
        ]

        return result

    @profile_execution_time
    def locate_text_in_sentences(
        self, sentences: list[TranscriptSentence], search_term: str
    ) -> list[SearchMediaLocation]:
        """Locate text in sentences."""

        sentences_texts = [sentence.text for sentence in sentences]

        prompt = (
            """
            You are given an array of sentences and a search term.
            Go over each sentence and decide how relvant the search term is to the topic of that sentence.

            Output an array of relantance scores for each sentence that indicates how relevant the search term is to the topic of that sentence.
            1 indicates that the search term is highly relevant to the topic of the sentence.
            0 indicates that the search term is not relevant to the topic of the sentence.

            Use this as input:
            sentences = """
            + str(sentences_texts)
            + """
            """
        )
        response = self.model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[float]
            ),
        )
        relevance_scores = json.loads(response.text)
        sorted_indices = sorted(
            range(len(relevance_scores)),
            key=lambda i: relevance_scores[i],
            reverse=True,
        )
        locations = [
            SearchMediaLocation(
                **sentences[sorted_index].model_dump(include={"start", "end"}),
                relevance=relevance_scores[sorted_index],
                search_term=search_term,
            )
            for sorted_index in sorted_indices
        ]

        return locations
