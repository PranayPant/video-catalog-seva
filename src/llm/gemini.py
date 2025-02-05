import json
import google.generativeai as genai

from ..custom_types import (
    TranscriptSentence,
    SearchMediaLocation,
)
from ..decorators import handle_exceptions, profile_execution_time, decorate_all_methods


@decorate_all_methods(profile_execution_time)
@decorate_all_methods(handle_exceptions)
class GenAI:

    DEFAULT_MODEL_NAME = "gemini-2.0-flash-exp"

    def __init__(self, model_name: str | None = None) -> None:
        self.model = genai.GenerativeModel(
            model_name=model_name or self.DEFAULT_MODEL_NAME,
        )

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

    def locate_text_in_sentences(
        self, sentences: list[TranscriptSentence], search_term: str
    ) -> list[SearchMediaLocation]:
        """Locate text in sentences."""

        sentences_texts = [sentence.text for sentence in sentences]

        prompt = (
            """
            You are given an array of sentences and a topic.

            Score each sentence based on how relevant it is to the given topic, and provide a justification for each score.
            The score should be a float between 0 and 1 with two digits precision, 
            and should indicate what percentage of the sentence content is related to the topic.

            Output an array of strings where each element has the form "score,justification".

            Use the following as input:
            
            sentences = """
            + str(sentences_texts)
            + """
            
            topoic = """
            + search_term
            + """"

            """
        )
        response = self.model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=list[str],
            ),
        )
        match_info = json.loads(response.text)
        sorted_indices = sorted(
            range(len(match_info)),
            key=lambda i: float(match_info[i].split(",")[0]),
            reverse=True,
        )
        locations = [
            SearchMediaLocation(
                **sentences[sorted_index].model_dump(include={"start", "end"}),
                relevance=float(match_info[sorted_index].split(",")[0]),
                justifications=match_info[sorted_index].split(",")[1],
                search_term=search_term,
                sentence=sentences[sorted_index].text,
            )
            for sorted_index in sorted_indices
        ]

        return locations
