from flask import Response
from flask.testing import FlaskClient


def test_get(client: FlaskClient):
    result: Response = client.get('/health-check')

    assert result.status_code == 200
