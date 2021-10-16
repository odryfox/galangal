import pytest
from config import Config
from flask.testing import FlaskClient
from web import create_app


@pytest.fixture(scope='module', autouse=True)
def client() -> FlaskClient:
    config = Config()
    app = create_app(config)

    with app.test_client() as client:
        yield client
