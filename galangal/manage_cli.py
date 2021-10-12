from cli import create_app
from config import EnvironmentConfig

config = EnvironmentConfig()
app = create_app(config=config)

if __name__ == '__main__':
    app.run()
