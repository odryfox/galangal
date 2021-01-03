from infrastructure.cli import create_app
from infrastructure.cli.config import EnvironmentConfig

config = EnvironmentConfig()
app = create_app(config=config)

if __name__ == '__main__':
    app.run()
