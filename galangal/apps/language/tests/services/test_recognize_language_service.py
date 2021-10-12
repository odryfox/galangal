import language.constants
import pytest
from language.services import RecognizeLanguageService


class TestRecognizeLanguageService:

    @classmethod
    def setup_class(cls):
        cls.service = RecognizeLanguageService()

    def test_execute__english_phrase(self):
        lang = self.service.execute(text='I will be back')

        assert lang == language.constants.Language.EN

    def test_execute__russian_phrase(self):
        lang = self.service.execute(text='Я вернусь')

        assert lang == language.constants.Language.RU

    def test_execute__multilingual_phrase(self):
        with pytest.raises(RecognizeLanguageService.MultilingualException):
            self.service.execute(text='I вернусь')

    def test_execute__non_specific_language_phrase(self):
        with pytest.raises(
            RecognizeLanguageService.NonSpecificLanguageException
        ):
            self.service.execute(text='!')
