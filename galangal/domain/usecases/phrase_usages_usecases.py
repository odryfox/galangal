from typing import List

from domain.constants import Language
from domain.entities import (
    PhraseToStudy,
    PhraseUsagesInDifferentLanguages,
    SearchPhrasesResponse
)
from domain.interfaces import (
    ILanguageService,
    IPhraseUsagesInDifferentLanguagesService
)


class SearchPhraseUsagesInDifferentLanguagesUsecase:

    def __init__(
        self,
        language_service: ILanguageService,
        phrase_usages_in_different_languages_service: IPhraseUsagesInDifferentLanguagesService,
    ) -> None:
        self.language_service = language_service
        self.phrase_usages_in_different_languages_service = phrase_usages_in_different_languages_service

    def execute(self, message: str) -> SearchPhrasesResponse:

        source_language = self.language_service.get_language(message)
        target_language = self._get_target_language(source_language)

        phrase_usages_in_different_languages = self.phrase_usages_in_different_languages_service.search(
            phrase=message,
            languages=[target_language],
            limit=5,
        )
        phrases_to_study = self._get_phrases_to_study_from_search(phrase_usages_in_different_languages)

        return SearchPhrasesResponse(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages,
            phrases_to_study=phrases_to_study,
        )

    def _get_target_language(self, source_language: Language) -> Language:
        return Language.RU if source_language is Language.EN else Language.EN

    def _get_phrases_to_study_from_search(
        self,
        phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages,
    ) -> List[PhraseToStudy]:

        if not phrase_usages_in_different_languages:
            return []

        languages = list(phrase_usages_in_different_languages[0].keys())

        source_language = languages[0]
        target_language = languages[1]

        phrases = set()
        for phrase_usage_in_different_languages in phrase_usages_in_different_languages:
            phrase_in_source_language = phrase_usage_in_different_languages[source_language].phrase.lower()
            phrase_in_target_language = phrase_usage_in_different_languages[target_language].phrase.lower()

            phrases.add((phrase_in_source_language, phrase_in_target_language))

        phrases_to_study = []
        for phrase in phrases:
            phrase_in_source_language = phrase[0]
            phrase_in_target_language = phrase[1]

            phrases_to_study.append(
                PhraseToStudy(
                    source_phrase=phrase_in_source_language,
                    target_phrase=phrase_in_target_language
                )
            )

        return phrases_to_study
