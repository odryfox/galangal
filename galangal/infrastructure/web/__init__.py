from domain.services import RegexLanguageService
from domain.usecases.phrase_to_study_usecases import (
    GetPhraseToStudyFromSearchUsecase
)
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from flask import Flask
from infrastructure.bot import create_agent
from infrastructure.bot.telegram import TelegramBot
from infrastructure.external import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from infrastructure.web.config import Config
from infrastructure.web.views import TelegramMessagesView, TelegramWebhooksView


def create_app(config: Config) -> Flask:

    regex_language_service = RegexLanguageService()
    telegram_bot = TelegramBot(token=config.TELEGRAM_TOKEN)

    phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
        language_service=regex_language_service,
    )

    search_phrase_usages_in_different_languages_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
        language_service=regex_language_service,
        phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
    )

    get_phrases_to_study_from_search_usecase = GetPhraseToStudyFromSearchUsecase()

    agent = create_agent(
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        get_phrases_to_study_from_search_usecase=get_phrases_to_study_from_search_usecase,
    )

    flask_app = Flask('web_app')
    add = flask_app.add_url_rule

    telegram_webhook_path = '/bot/messages/{}'.format(config.TELEGRAM_TOKEN)
    telegram_webhook_url = '{}{}'.format(
        config.TELEGRAM_WEBHOOK_BASE_URL, telegram_webhook_path
    )

    add(telegram_webhook_path, view_func=TelegramMessagesView.as_view(
        'bot_messages',
        agent=agent,
        telegram_bot=telegram_bot,
    ))

    add('/bot/webhooks', view_func=TelegramWebhooksView.as_view(
        'bot_webhooks',
        telegram_bot=telegram_bot,
        telegram_webhook_url=telegram_webhook_url,
    ))

    return flask_app
