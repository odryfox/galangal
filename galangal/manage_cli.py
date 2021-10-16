from cli import create_app
from config import Config

config = Config()
app = create_app(config=config)

if __name__ == '__main__':
    app.run()
