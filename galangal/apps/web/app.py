from config import Config
from flask import Flask
from web.views import HealthCheckView


def create_app(config: Config):
    flask_app = Flask('web_app')
    add = flask_app.add_url_rule

    add('/health-check', view_func=HealthCheckView.as_view('Health Check'))

    return flask_app
