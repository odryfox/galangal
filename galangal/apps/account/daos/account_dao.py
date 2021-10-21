from account.models import AccountModel
from db.connection import Session


class AccountDAO:

    def create_account_by_chat_id(self, chat_id: str):
        session = Session()

        instance = session.query(AccountModel).filter_by(
            chat_id=chat_id,
        ).one_or_none()
        if instance:
            return

        account_model = AccountModel(chat_id=chat_id)

        try:
            session.add(account_model)
            session.commit()
        except Exception:
            session.rollback()
