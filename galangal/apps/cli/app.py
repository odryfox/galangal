from bot.messengers.cli import CLIProcessMessageService


class App:
    def __init__(self):
        self.process_message_service = CLIProcessMessageService()

    def run(self):
        process_message_service = CLIProcessMessageService()
        message = None
        while True:
            process_message_service.execute(message)
            message = input()

            if message in (':quit', ':q'):
                break


def create_app():
    return App()
