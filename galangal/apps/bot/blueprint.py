import bot.constants
from bot.views import TelegramProcessMessageView, TelegramRegisterWebhookView
from flask import Blueprint

blueprint = Blueprint('Bot', __name__)
add = blueprint.add_url_rule


add(bot.constants.TELEGRAM_WEBHOOK_PATH, view_func=TelegramProcessMessageView.as_view(
    'bot_messages',
))

add('/bot/webhooks', view_func=TelegramRegisterWebhookView.as_view(
    'bot_webhooks',
))
