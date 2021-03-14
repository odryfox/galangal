from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class PhraseORM(Base):
    __tablename__ = 'phrases'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False, unique=True)

    source_synonyms = relationship(
        'SynonymORM', back_populates='source_phrase',
        foreign_keys='[SynonymORM.source_phrase_id]',
    )
    target_synonyms = relationship(
        'SynonymORM', back_populates='target_phrase',
        foreign_keys='[SynonymORM.target_phrase_id]',
    )


class SynonymORM(Base):
    __tablename__ = 'synonyms'

    id = Column(Integer, primary_key=True)

    source_phrase_id = Column(Integer, ForeignKey('phrases.id'))
    source_phrase = relationship('PhraseORM', back_populates='source_synonyms', foreign_keys=[source_phrase_id])

    target_phrase_id = Column(Integer, ForeignKey('phrases.id'))
    target_phrase = relationship('PhraseORM', back_populates='target_synonyms', foreign_keys=[target_phrase_id])

    study_synonyms = relationship('StudySynonymORM', back_populates='synonym')

    __table_args__ = (
        UniqueConstraint(
            'source_phrase_id',
            'target_phrase_id',
            name='source_target_phrases_unique',
        ),
    )


class AccountORM(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    telegram_chat_id = Column(String, nullable=False, unique=True)

    study_synonyms = relationship('StudySynonymORM', back_populates='account')


class StudySynonymORM(Base):
    __tablename__ = 'study_synonyms'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('AccountORM', back_populates='study_synonyms')

    synonym_id = Column(Integer, ForeignKey('synonyms.id'))
    synonym = relationship('SynonymORM', back_populates='study_synonyms')

    __table_args__ = (
        UniqueConstraint(
            'account_id',
            'synonym_id',
            name='account_synonym_unique',
        ),
    )
