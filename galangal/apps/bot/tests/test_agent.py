from unittest import mock

from account.daos import AccountDAO
from account.models import AccountModel
from account.testing.factories import AccountModelFactory
from bot.agent import create_agent
from bot.constants import ActionType
from bot.markdown import Action
from redis_client import Redis


def test_agent__greeting_without_account(redis: Redis, session):
    action = Action(action_type=ActionType.GREETING, params={})
    agent = create_agent()
    answers = agent.query(action, user_id='test')

    assert answers == [
        'Привет, я бот, который поможет тебе выучить язык быстро',
        'Как я могу тебя называть?',
    ]

    answers = agent.query('Bob', user_id='test')

    assert answers == [
        'Bob, очень приятно познакомиться)',
        (
            'А теперь давай перейдем в режим перевода слов. '
            'Просто введи интересующее тебя слово или фразу и я переведу ее.'
        ),
    ]

    account = session.query(AccountModel).filter_by(chat_id='test').first()
    assert account.username == 'Bob'


def test_agent__greeting_with_account(redis: Redis, session):
    AccountModelFactory(chat_id='test', username='Bob')

    action = Action(action_type=ActionType.GREETING, params={})
    agent = create_agent()
    answers = agent.query(action, user_id='test')

    assert answers == [
        'Привет, я бот, который поможет тебе выучить язык быстро',
        (
            'А теперь давай перейдем в режим перевода слов. '
            'Просто введи интересующее тебя слово или фразу и я переведу ее.'
        ),
    ]


@mock.patch.object(AccountDAO, 'is_account_exists')
@mock.patch.object(AccountDAO, 'create_account_by_chat_id')
def test_agent__correct_calls(
    create_account_by_chat_id_mock, is_account_exists_mock,
    redis: Redis, session
):
    is_account_exists_mock.return_value = False

    action = Action(action_type=ActionType.GREETING, params={})
    agent = create_agent()
    answers = agent.query(action, user_id='test')

    assert answers == [
        'Привет, я бот, который поможет тебе выучить язык быстро',
        'Как я могу тебя называть?',
    ]

    answers = agent.query('Bob', user_id='test')

    assert answers == [
        'Bob, очень приятно познакомиться)',
        (
            'А теперь давай перейдем в режим перевода слов. '
            'Просто введи интересующее тебя слово или фразу и я переведу ее.'
        ),
    ]

    is_account_exists_mock.assert_called_once_with(
        mock.ANY,
        chat_id='test',
    )
    create_account_by_chat_id_mock.assert_called_once_with(
        mock.ANY,
        chat_id='test',
        username='Bob',
    )
