from unittest import mock

from infrastructure.web import create_app
from infrastructure.web.config import TestEnvironmentConfig


class TestHealthCheckView:

    @classmethod
    def setup_class(cls):
        config = TestEnvironmentConfig()

        with mock.patch('infrastructure.telegram.bot.Updater') as updater_mock:
            cls.updater_bot = mock.Mock()
            updater_mock.return_value = mock.Mock(bot=cls.updater_bot)
            app = create_app(config=config)

        cls.client = app.test_client()

    def test_get(self):
        response = self.client.get('/health-check')

        assert response.status_code == 200
