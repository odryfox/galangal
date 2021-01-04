from infrastructure.web import create_app
from infrastructure.web.config import TestEnvironmentConfig


class TestHealthCheckView:

    @classmethod
    def setup_class(cls):
        config = TestEnvironmentConfig()
        app = create_app(config=config)
        cls.client = app.test_client()

    def test_get(self):
        response = self.client.get('/health-check')

        assert response.status_code == 200
