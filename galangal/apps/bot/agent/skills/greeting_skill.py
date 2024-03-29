from account.daos import AccountDAO
from millet import BaseSkill


class GreetingSkill(BaseSkill):

    side_methods = [
        (AccountDAO, 'is_account_exists'),
        (AccountDAO, 'create_account_by_chat_id'),
    ]

    def execute(self, message: str, user_id: str) -> str:
        self.say('Привет, я бот, который поможет тебе выучить язык быстро')

        is_account_exists = AccountDAO().is_account_exists(
            chat_id=user_id,
        )

        if not is_account_exists:
            username = self.ask('Как я могу тебя называть?')

            AccountDAO().create_account_by_chat_id(
                chat_id=user_id,
                username=username,
            )

            self.say(f'{username}, очень приятно познакомиться)')

        return (
            'А теперь давай перейдем в режим перевода слов. '
            'Просто введи интересующее тебя слово или фразу и я переведу ее.'
        )
