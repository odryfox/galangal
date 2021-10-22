import sqlalchemy
from db import Base
from sqlalchemy.orm import relationship


class AccountModel(Base):
    __tablename__ = 'accounts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    chat_id = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    phrases_to_study = relationship(
        'PhraseToStudyModel', back_populates='account',
        foreign_keys='[PhraseToStudyModel.account_id]',
    )
