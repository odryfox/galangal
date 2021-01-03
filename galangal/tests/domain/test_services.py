from domain.constants import Language
from domain.services import RegexLanguageService


class TestRegexLanguageService:

    @classmethod
    def setup_class(cls):
        cls.service = RegexLanguageService()

    def test_english_phrase(self):
        language = self.service.get_language(text='I will be back')

        assert language == Language.EN

    def test_russian_phrase(self):
        language = self.service.get_language(text='Я вернусь')

        assert language == Language.RU

    def test_multilingual_phrase(self):
        language = self.service.get_language(text='I вернусь')

        assert language == Language.RU
