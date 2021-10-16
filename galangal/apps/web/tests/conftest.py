import pytest
from flask import Flask
from flask.testing import FlaskClient
from web.views import HealthCheckView


@pytest.fixture(autouse=True)
def client() -> FlaskClient:
    app = Flask(__name__)
    add = app.add_url_rule
    add('/health-check', view_func=HealthCheckView.as_view('Health Check'))

    with app.test_client() as client:
        yield client
