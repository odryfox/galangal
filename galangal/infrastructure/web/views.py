from flask import request
from flask.views import MethodView
from infrastructure.bot import TelegramService
from millet import Agent


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
        agent: Agent,
        telegram_service: TelegramService,
    ):
        self._agent = agent
        self._telegram_service = telegram_service

        super().__init__()

    def post(self):

        body = request.get_json()
        try:
            chat_id = body['message']['chat']['id']
            message = body['message']['text']
        except KeyError:
            chat_id = body['callback_query']['from']['id']
            word = body['callback_query']['data']
            self._telegram_service.send_message(chat_id, 'Слово {} добавлено на изучение'.format(word))
            return '!'

        answers = self._agent.query(message, chat_id)

        for answer in answers:
            self._telegram_service.send_phrase_usages_in_different_languages(
                chat_id=chat_id,
                phrase_usages_in_different_languages=answer,
                languages=[],
            )

        return '!'
