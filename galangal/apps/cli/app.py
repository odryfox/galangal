from config import Config


class App:
    def __init__(self, config: Config):
        pass

    def run(self):
        while True:
            request = input()
            print(request)


def create_app(config: Config):
    return App(config=config)
