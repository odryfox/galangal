from unittest import mock

import pytest
from language.constants import Language
from language.services import RecognizeLanguageService
from search_phrase_contexts.daos import PhraseContextsDAO
from search_phrase_contexts.entities import PhraseContext
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase


class TestSearchPhraseContextsUseCase:

    def setup_method(self):
        self.phrase_contexts_dao = mock.Mock(spec=PhraseContextsDAO)
        self.use_case = SearchPhraseContextsUseCase(
            recognize_language_service=RecognizeLanguageService(),
            phrase_contexts_dao=self.phrase_contexts_dao,
        )

    def test_execute__usual_phrase(self):
        phrase_contexts_expected = [
            PhraseContext(
                source_language_phrase='I will be back',
                source_language_context='If anyone should phone, say I will be back at one o\'clock.',
                target_language_phrase='я вернусь',
                target_language_context='Если кто-нибудь позвонит, скажи, что я вернусь в час.',
            ),
            PhraseContext(
                source_language_phrase='I will be back',
                source_language_context='I will be back by 5, but just...',
                target_language_phrase='Я вернусь',
                target_language_context='Я вернусь к пяти, но если...',
            ),
        ]
        self.phrase_contexts_dao.search_phrase_contexts.return_value = (
            phrase_contexts_expected
        )

        phrase_contexts_actual = self.use_case.execute(
            phrase='I will be back',
        )

        assert (
            phrase_contexts_actual == phrase_contexts_expected
        )

        self.phrase_contexts_dao.search_phrase_contexts.assert_called_once_with(
            phrase='I will be back',
            source_language=Language.EN,
            target_language=Language.RU,
            limit=5,
        )

    def test_execute__multilingual_phrase(self):
        with pytest.raises(SearchPhraseContextsUseCase.MultilingualException):
            self.use_case.execute(
                phrase='I вернусь',
            )

        self.phrase_contexts_dao.search_phrase_contexts.assert_not_called()

    def test_execute__non_specific_language_phrase(self):
        with pytest.raises(
            SearchPhraseContextsUseCase.NonSpecificLanguageException
        ):
            self.use_case.execute(
                phrase='!',
            )

        self.phrase_contexts_dao.search_phrase_contexts.assert_not_called()
