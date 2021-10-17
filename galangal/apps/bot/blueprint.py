import settings
from bot.agent.agent import create_agent
from bot.daos import CallbackDataDAO
from bot.messengers.telegram.process_message_service import (
    TelegramProcessMessageService
)
from bot.views import TelegramProcessMessageView, TelegramRegisterWebhookView
from flask import Blueprint
from language.services import RecognizeLanguageService
from redis import Redis
from search_phrase_contexts.daos import PhraseContextsDAO
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase
from vocabulary_trainer.daos import PhraseToStudyDAO
from vocabulary_trainer.use_cases import (
    AddPhraseToStudyUseCase,
    SuggestPhrasesToStudyUseCase
)

blueprint = Blueprint('Bot', __name__)
add = blueprint.add_url_rule

telegram_webhook_path = '/bot/messages/{}'.format(settings.TELEGRAM_TOKEN)

redis = Redis.from_url(settings.REDIS_URL)

agent = create_agent(
    add_phrase_to_study_use_case=AddPhraseToStudyUseCase(
        phrase_to_study_dao=PhraseToStudyDAO(),
    ),
    search_phrase_contexts_use_case=SearchPhraseContextsUseCase(
        recognize_language_service=RecognizeLanguageService(),
        phrase_contexts_dao=PhraseContextsDAO(),
    ),
    suggest_phrases_to_study_use_case=SuggestPhrasesToStudyUseCase(),
    redis=redis,
)

telegram_process_message_service = TelegramProcessMessageService(
    token=settings.TELEGRAM_TOKEN,
    agent=agent,
    callback_data_dao=CallbackDataDAO(redis=redis),
)

add(telegram_webhook_path, view_func=TelegramProcessMessageView.as_view(
    'bot_messages',
    telegram_process_message_service=telegram_process_message_service,
))

add('/bot/webhooks', view_func=TelegramRegisterWebhookView.as_view(
    'bot_webhooks',
    telegram_webhook_path=telegram_webhook_path,
))
