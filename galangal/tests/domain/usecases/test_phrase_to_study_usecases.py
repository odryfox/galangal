from domain.constants import Language
from domain.entities import PhraseToStudy, PhraseUsage
from domain.usecases.phrase_to_study_usecases import (
    GetPhraseToStudyFromSearchUsecase
)


class TestGetPhraseToStudyFromSearchUsecase:

    @classmethod
    def setup_class(cls):
        cls.usecase = GetPhraseToStudyFromSearchUsecase()

    def test_execute__filter_duplicates(self):
        phrase_usages_in_different_languages = [
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

        actual_result = self.usecase.execute(
            phrase_usages_in_different_languages=phrase_usages_in_different_languages
        )

        expected_result = [
            PhraseToStudy(
                source_phrase='i will be back',
                target_phrase='я вернусь',
            )
        ]

        assert actual_result == expected_result
