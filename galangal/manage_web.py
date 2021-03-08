from infrastructure.web import create_app
from infrastructure.web.config import EnvironmentConfig

config = EnvironmentConfig()
app = create_app(config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
