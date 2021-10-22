import factory
from account.models import AccountModel
from db.connection import Session


class AccountModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AccountModel
        sqlalchemy_session = Session()
        sqlalchemy_get_or_create = ('chat_id',)
        sqlalchemy_session_persistence = 'commit'

    chat_id = '100500'
    username = 'Doe'
