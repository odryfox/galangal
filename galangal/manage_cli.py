from infrastructure.cli import App
from infrastructure.cli.config import EnvironmentConfig

config = EnvironmentConfig()
app = App(config=config)

if __name__ == '__main__':
    app.run()
