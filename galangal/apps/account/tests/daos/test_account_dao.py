from account.daos import AccountDAO
from account.models import AccountModel


def test_create_account_by_chat_id(session):
    dao = AccountDAO()
    dao.create_account_by_chat_id(chat_id='example')

    count = session.query(AccountModel).count()
    assert count == 1
