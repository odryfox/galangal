import pytest
from flask.testing import FlaskClient
from web import create_app


@pytest.fixture(autouse=True)
def client() -> FlaskClient:
    app = create_app()

    with app.test_client() as client:
        yield client
