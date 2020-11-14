from domain.usecases.bot_usecases import RegisterBotWebhookUsecase
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from flask import request
from flask.views import MethodView


class TelegramWebhooksView(MethodView):
    def __init__(self, register_telegram_webhook_usecase: RegisterBotWebhookUsecase) -> None:
        self._register_telegram_webhook_usecase = register_telegram_webhook_usecase

        super().__init__()

    def get(self):
        self._register_telegram_webhook_usecase.execute()
        return '!'


class TelegramMessagesView(MethodView):
    def __init__(self, search_phrase_usages_in_different_languages_usecase: SearchPhraseUsagesInDifferentLanguagesUsecase):
        self._search_phrase_usages_in_different_languages_usecase = search_phrase_usages_in_different_languages_usecase

        super().__init__()

    def post(self):
        try:
            body = request.get_json()
            chat_id = body['message']['chat']['id']
            message = body['message']['text']
            self._search_phrase_usages_in_different_languages_usecase.execute(
                chat_id=chat_id,
                message=message
            )
        except Exception:
            pass
        return '!'
