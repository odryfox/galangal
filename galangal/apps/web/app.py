from flask import Flask
from web.views import HealthCheckView


def create_app():
    flask_app = Flask('web_app')

    from bot.blueprint import blueprint as bot_blueprint
    flask_app.register_blueprint(bot_blueprint)

    add = flask_app.add_url_rule
    add('/health-check', view_func=HealthCheckView.as_view('Health Check'))

    return flask_app
