from infrastructure.web import create_app
from infrastructure.web.config import EnvironmentConfig


class TestHealthCheckView:

    @classmethod
    def setup_class(cls):
        config = EnvironmentConfig()
        app = create_app(config=config)
        cls.client = app.test_client()

    def test_get(self):
        response = self.client.get('/health-check')

        assert response.status_code == 200
