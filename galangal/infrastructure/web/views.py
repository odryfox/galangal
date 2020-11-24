from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from flask import request
from flask.views import MethodView
from infrastructure.bot import TelegramService


class TelegramWebhooksView(MethodView):
    def __init__(
        self,
        telegram_service: TelegramService,
        telegram_webhook_url: str,
    ) -> None:
        self._telegram_service = telegram_service
        self._telegram_webhook_url = telegram_webhook_url

        super().__init__()

    def get(self):
        self._telegram_service.register_webhook(self._telegram_webhook_url)
        return '!'


class TelegramMessagesView(MethodView):
    def __init__(
        self,
        search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase,
        telegram_service: TelegramService,
    ):
        self._search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase
        self._telegram_service = telegram_service

        super().__init__()

    def post(self):

        body = request.get_json()
        chat_id = body['message']['chat']['id']
        message = body['message']['text']

        try:
            phrase_usages_in_different_languages = self._search_phrase_usages_in_different_languages_usecase.execute(
                message=message
            )
        except:
            self._telegram_service.send_message(
                chat_id=chat_id,
                message='Произошла ошибка, обратись к создателю бота',
            )
        else:

            if phrase_usages_in_different_languages:
                self._telegram_service.send_phrase_usages_in_different_languages(
                    chat_id=chat_id,
                    phrase_usages_in_different_languages=phrase_usages_in_different_languages,
                    languages=list(phrase_usages_in_different_languages[0].keys()),
                )
            else:
                self._telegram_service.send_message(
                    chat_id=chat_id,
                    message='Увы, но я не нашел употреблений этой фразы :(',
                )

        return '!'
