from domain.agent import create_agent
from domain.services import RegexLanguageService
from domain.usecases.phrase_usages_usecases import (
    SearchPhraseUsagesInDifferentLanguagesUsecase
)
from domain.usecases.save_phrase_to_study import SavePhraseToStudyUsecase
from flask import Flask
from infrastructure.db.connection import DB
from infrastructure.db.phrase_dao import DBPhraseDAO
from infrastructure.redis.callback_data_dao import RedisCallbackDataDAO
from infrastructure.telegram.bot import TelegramBot
from infrastructure.third_party.reverso import (
    ReversoContextPhraseUsagesInDifferentLanguagesService
)
from infrastructure.web.config import Config
from infrastructure.web.views import (
    HealthCheckView,
    TelegramMessagesView,
    TelegramWebhooksView
)
from redis import Redis


def create_app(config: Config) -> Flask:

    regex_language_service = RegexLanguageService()
    phrase_usages_in_different_languages_service = ReversoContextPhraseUsagesInDifferentLanguagesService(
        language_service=regex_language_service,
    )
    search_phrase_usages_in_different_languages_usecase = SearchPhraseUsagesInDifferentLanguagesUsecase(
        language_service=regex_language_service,
        phrase_usages_in_different_languages_service=phrase_usages_in_different_languages_service,
    )

    db = DB(url=config.DATABASE_URL)
    session = db.create_session()
    phrase_dao = DBPhraseDAO(session=session)
    save_phrase_to_study_usecase = SavePhraseToStudyUsecase(phrase_dao=phrase_dao)

    agent = create_agent(
        search_phrase_usages_in_different_languages_usecase=search_phrase_usages_in_different_languages_usecase,
        save_phrase_to_study_usecase=save_phrase_to_study_usecase,
        phrase_dao=phrase_dao,
    )

    redis = Redis.from_url(config.REDIS_URL)
    callback_data_dao = RedisCallbackDataDAO(redis=redis)
    telegram_bot = TelegramBot(
        token=config.TELEGRAM_TOKEN,
        agent=agent,
        callback_data_dao=callback_data_dao,
    )

    flask_app = Flask('web_app')
    add = flask_app.add_url_rule

    telegram_webhook_path = '/bot/messages/{}'.format(config.TELEGRAM_TOKEN)
    telegram_webhook_url = '{}{}'.format(
        config.TELEGRAM_WEBHOOK_BASE_URL, telegram_webhook_path
    )

    add(telegram_webhook_path, view_func=TelegramMessagesView.as_view(
        'bot_messages',
        telegram_bot=telegram_bot,
    ))

    add('/bot/webhooks', view_func=TelegramWebhooksView.as_view(
        'bot_webhooks',
        telegram_bot=telegram_bot,
        telegram_webhook_url=telegram_webhook_url,
    ))

    add('/health-check', view_func=HealthCheckView.as_view('Health Check'))

    return flask_app
