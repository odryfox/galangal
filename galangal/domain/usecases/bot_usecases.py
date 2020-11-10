from domain.interfaces import IBotService


class RegisterBotWebhookUsecase:
    def __init__(self, bot_service: IBotService) -> None:
        self._bot_service = bot_service

    def execute(self, url: str) -> None:
        self._bot_service.register_webhook(url=url)
