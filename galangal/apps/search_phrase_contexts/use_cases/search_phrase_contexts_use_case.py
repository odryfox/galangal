from typing import List

import language.constants
from language.services import RecognizeLanguageService
from search_phrase_contexts.daos import PhraseContextsDAO
from search_phrase_contexts.entities import PhraseContext


class SearchPhraseContextsUseCase:

    CONTEXTS_LIMIT = 5

    class MultilingualException(Exception):
        pass

    class NonSpecificLanguageException(Exception):
        pass

    def __init__(
        self,
        recognize_language_service: RecognizeLanguageService,
        phrase_contexts_dao: PhraseContextsDAO,
    ) -> None:
        self.recognize_language_service = recognize_language_service
        self.phrase_contexts_dao = phrase_contexts_dao

    def execute(
        self,
        phrase: str,
    ) -> List[PhraseContext]:

        try:
            source_language = self.recognize_language_service.execute(phrase)
        except RecognizeLanguageService.MultilingualException:
            raise self.MultilingualException
        except RecognizeLanguageService.NonSpecificLanguageException:
            raise self.NonSpecificLanguageException

        if source_language == language.constants.Language.RU:
            target_language = language.constants.Language.EN
        else:
            target_language = language.constants.Language.RU

        phrase_contexts = self.phrase_contexts_dao.search_phrase_contexts(
            phrase=phrase,
            source_language=source_language,
            target_language=target_language,
            limit=self.CONTEXTS_LIMIT,
        )
        return phrase_contexts


def create_search_phrase_contexts_use_case() -> SearchPhraseContextsUseCase:
    return SearchPhraseContextsUseCase(
        recognize_language_service=RecognizeLanguageService(),
        phrase_contexts_dao=PhraseContextsDAO(),
    )
