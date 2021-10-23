from account.models import AccountModel
from db.connection import Session


class AccountDAO:

    def is_account_exists(self, chat_id: str):
        session = Session()

        instance = session.query(AccountModel).filter_by(
            chat_id=chat_id,
        ).one_or_none()
        return bool(instance)

    def create_account_by_chat_id(self, chat_id: str, username: str):
        session = Session()

        instance = session.query(AccountModel).filter_by(
            chat_id=chat_id,
        ).one_or_none()
        if instance:
            return

        account_model = AccountModel(chat_id=chat_id, username=username)

        try:
            session.add(account_model)
            session.commit()
        except Exception:
            session.rollback()
