from flask import request
from flask.views import MethodView


class BotWebhooksView(MethodView):
    def __init__(self, web_app) -> None:
        self._bot_message_url = web_app.bot_message_url
        self._register_webhook_usecase = web_app.register_webhook_usecase

        super().__init__()

    def get(self):
        self._register_webhook_usecase.execute(url=self._bot_message_url)
        return '!'


class BotMessagesView(MethodView):
    def __init__(self, web_app):
        self._search_usage_collocations_usecase = web_app.search_usage_collocations_usecase

        super().__init__()

    def post(self):
        try:
            body = request.get_json()
            chat_id = body['message']['chat']['id']
            message = body['message']['text']
            self._search_usage_collocations_usecase.execute(
                chat_id=chat_id,
                message=message
            )
        except Exception:
            pass
        return '!'
