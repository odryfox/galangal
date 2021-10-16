from unittest import mock
from unittest.mock import patch

import pytest
import settings
from flask.testing import FlaskClient
from web import create_app


@pytest.fixture()
def telegram_process_message_service_class():
    telegram_process_message_service_class_mock = mock.Mock()
    with patch('web.app.TelegramProcessMessageService', autospec=True):
        yield telegram_process_message_service_class_mock


@pytest.fixture()
def telegram_register_webhook_service_class():
    telegram_register_webhook_service_class_mock = mock.Mock()
    with patch('web.app.TelegramRegisterWebhookService', autospec=True):
        yield telegram_register_webhook_service_class_mock


@pytest.fixture(autouse=True)
def client(telegram_process_message_service_class, telegram_register_webhook_service_class) -> FlaskClient:
    app = create_app()

    with app.test_client() as client:
        yield client
