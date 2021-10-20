from account.models import AccountModel
from db.connection import Session


class AccountDAO:

    def create_account_by_chat_id(self, chat_id: str):
        session = Session()

        account_model = AccountModel(chat_id=chat_id)

        session.add(account_model)
        session.commit()
