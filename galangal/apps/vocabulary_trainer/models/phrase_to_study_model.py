import sqlalchemy
from db import Base
from sqlalchemy.orm import relationship


class PhraseToStudyModel(Base):
    __tablename__ = 'phrases'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    account_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('accounts.id')
    )
    account = relationship(
        'AccountModel', back_populates='phrases_to_study',
        foreign_keys=[account_id]
    )

    source_language_phrase = sqlalchemy.Column(
        sqlalchemy.String, nullable=False, unique=True
    )
    target_language_phrase = sqlalchemy.Column(
        sqlalchemy.String, nullable=False, unique=True
    )
