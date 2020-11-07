import re

from domain.constants import LanguageEnum
from domain.interfaces import ITelegramService, IUsageCollocationsService


class RegisterWebhookUsecase:
    def __init__(self, telegram_service: ITelegramService) -> None:
        self._telegram_service = telegram_service

    def execute(self, url: str) -> None:
        self._telegram_service.register_webhook(url=url)


class SearchUsageCollocationsUsecase:
    def __init__(
            self, usage_collocations_service: IUsageCollocationsService,
            telegram_service: ITelegramService
    ) -> None:
        self._usage_collocations_service = usage_collocations_service
        self._telegram_service = telegram_service

    def _get_source_language(self, message: str) -> LanguageEnum:
        if bool(re.search('[а-яА-Я]', message)):
            language = LanguageEnum.RU
        else:
            language = LanguageEnum.EN
        return language

    def _get_target_language(self, source_language: LanguageEnum) -> LanguageEnum:
        if source_language == LanguageEnum.EN:
            language = LanguageEnum.RU
        else:
            language = LanguageEnum.EN
        return language

    def execute(self, chat_id: str, message: str) -> None:
        try:
            source_language = self._get_source_language(message)
            target_language = self._get_target_language(source_language)

            usage_collocations = self._usage_collocations_service.search(
                collocation=message,
                source_language=source_language,
                target_language=target_language,
                limit=5,
            )

            response = ''
            for usage_collocation in usage_collocations:
                collocation = usage_collocation[target_language]
                parts = collocation.sentence.split(collocation.collocation_from_sentence)
                target_text = "*{}*".format(collocation.collocation_from_sentence).join(parts)
                response += target_text + '\n'

                collocation = usage_collocation[source_language]
                parts = collocation.sentence.split(collocation.collocation_from_sentence)
                target_text = "*{}*".format(collocation.collocation_from_sentence).join(parts)
                response += target_text + '\n\n'
        except Exception:
            response = ''

        if not response:
            response = 'Произошла ошибка('

        self._telegram_service.send_message(
            chat_id=chat_id,
            message=response,
        )
