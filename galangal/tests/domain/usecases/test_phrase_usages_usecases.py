from unittest import mock

from domain.constants import Language
from domain.entities import PhraseUsage
from domain.interfaces import IPhraseUsagesInDifferentLanguagesService
from domain.services import RegexLanguageService
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)


class TestSearchPhraseUsagesInDifferentLanguagesUsecase:

    def setup_method(self):
        self.phrase_usages_in_different_languages_service = mock.Mock(
            spec=IPhraseUsagesInDifferentLanguagesService
        )
        self.usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
            language_service=RegexLanguageService(),
            phrase_usages_in_different_languages_service=self.phrase_usages_in_different_languages_service,
        )

    def test_usual_result(self):
        expected_result = [
            {
                Language.EN: PhraseUsage(
                    text="If anyone should phone, say I will be back at one o'clock.",
                    phrase='I will be back',
                ),
                Language.RU: PhraseUsage(
                    text='Если кто-нибудь позвонит, скажи, что я вернусь в час.',
                    phrase='я вернусь',
                ),
            },
            {
                Language.EN: PhraseUsage(
                    text='I will be back by 5, but just...',
                    phrase='I will be back',
                ),
                Language.RU: PhraseUsage(
                    text='Я вернусь к пяти, но если...',
                    phrase='Я вернусь',
                ),
            },
        ]
        self.phrase_usages_in_different_languages_service.search.return_value = expected_result
        message = 'I will be back'

        actual_result = self.usecase.execute(message=message)

        assert actual_result == expected_result

        self.phrase_usages_in_different_languages_service.search.assert_called_once_with(
            phrase=message,
            languages=[Language.RU],
            limit=5,
        )

    def test_empty_result(self):
        expected_result = []
        self.phrase_usages_in_different_languages_service.search.return_value = expected_result
        message = 'Я вернусь'

        actual_result = self.usecase.execute(message=message)

        assert actual_result == expected_result

        self.phrase_usages_in_different_languages_service.search.assert_called_once_with(
            phrase=message,
            languages=[Language.EN],
            limit=5,
        )
