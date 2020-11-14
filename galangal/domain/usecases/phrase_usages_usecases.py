from domain.constants import Language
from domain.interfaces import (IBotService, ILanguageService,
                               IPhraseUsagesInDifferentLanguagesService)


class SearchPhraseUsagesInDifferentLanguagesUsecase:

    def __init__(
        self,
        language_service: ILanguageService,
        phrase_usages_in_different_languages_service: IPhraseUsagesInDifferentLanguagesService,
        bot_service: IBotService
    ) -> None:
        self._language_service = language_service
        self._phrase_usages_in_different_languages_service = phrase_usages_in_different_languages_service
        self._bot_service = bot_service

    def _get_target_language(self, source_language: Language) -> Language:
        return Language.RU if source_language is Language.EN else Language.EN

    def execute(self, chat_id: str, message: str) -> None:

        source_language = self._language_service.get_language(message)
        target_language = self._get_target_language(source_language)

        try:
            phrase_usages_in_different_languages = self._phrase_usages_in_different_languages_service.search(
                phrase=message,
                languages=[target_language],
                limit=5,
            )
        except:
            self._bot_service.send_message(
                chat_id=chat_id,
                message='Произошла ошибка, обратись к создателю бота',
            )
            return

        if phrase_usages_in_different_languages:
            self._bot_service.send_phrase_usages_in_different_languages(
                chat_id=chat_id,
                phrase_usages_in_different_languages=phrase_usages_in_different_languages,
                languages=[target_language, source_language],
            )
        else:
            self._bot_service.send_message(
                chat_id=chat_id,
                message='Увы, но я не нашел употреблений этой фразы :(',
            )
