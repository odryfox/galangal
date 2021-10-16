from config import Config
from web import create_app

config = Config()
app = create_app(config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
