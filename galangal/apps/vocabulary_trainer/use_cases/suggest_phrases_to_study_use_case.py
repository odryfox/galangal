from typing import List

from search_phrase_contexts.entities import PhraseContext
from vocabulary_trainer.entities import PhraseToStudy


class SuggestPhrasesToStudyUseCase:

    def _clean_phrase(self, phrase: str) -> str:
        return phrase.lower()

    def execute(
        self,
        phrase_contexts: List[PhraseContext],
    ) -> List[PhraseToStudy]:

        suggestions_phrases_to_study = []

        for phrase_context in phrase_contexts:
            source_language_phrase_cleaned = (
                self._clean_phrase(phrase_context.source_language_phrase)
            )
            target_language_phrase_cleaned = (
                self._clean_phrase(phrase_context.target_language_phrase)
            )

            suggestion_phrase_to_study = PhraseToStudy(
                source_language_phrase=source_language_phrase_cleaned,
                target_language_phrase=target_language_phrase_cleaned,
            )
            if suggestion_phrase_to_study not in suggestions_phrases_to_study:
                suggestions_phrases_to_study.append(suggestion_phrase_to_study)

        return suggestions_phrases_to_study


def create_suggest_phrases_to_study_use_case() -> SuggestPhrasesToStudyUseCase:
    return SuggestPhrasesToStudyUseCase()
