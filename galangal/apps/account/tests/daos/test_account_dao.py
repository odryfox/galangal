from account.daos import AccountDAO
from account.models import AccountModel
from account.testing.factories import AccountModelFactory


def test_is_account_exists__false():
    dao = AccountDAO()
    is_account_exists = dao.is_account_exists(chat_id='example')

    assert not is_account_exists


def test_is_account_exists__true():
    AccountModelFactory(chat_id='example')

    dao = AccountDAO()
    is_account_exists = dao.is_account_exists(chat_id='example')

    assert is_account_exists


def test_create_account_by_chat_id(session):
    dao = AccountDAO()
    dao.create_account_by_chat_id(chat_id='example', username='Bob')

    count = session.query(AccountModel).count()
    assert count == 1


def test_create_account_by_chat_id__already_exists(session):
    AccountModelFactory(chat_id='example')

    dao = AccountDAO()
    dao.create_account_by_chat_id(chat_id='example', username='Bob')

    count = session.query(AccountModel).count()
    assert count == 1
