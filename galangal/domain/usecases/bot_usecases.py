from domain.interfaces import IBotService


class RegisterBotWebhookUsecase:
    def __init__(self, bot_message_url: str, bot_service: IBotService) -> None:
        self._bot_message_url = bot_message_url
        self._bot_service = bot_service

    def execute(self) -> None:
        self._bot_service.register_webhook(url=self._bot_message_url)
