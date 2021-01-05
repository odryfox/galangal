from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class PhraseORM(Base):
    __tablename__ = 'phrases'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False, unique=True)

    source_links = relationship('PhraseLinkORM', back_populates='source_phrase', foreign_keys='[PhraseLinkORM.source_phrase_id]')
    target_links = relationship('PhraseLinkORM', back_populates='target_phrase', foreign_keys='[PhraseLinkORM.target_phrase_id]')


class PhraseLinkORM(Base):
    __tablename__ = 'phrase_links'

    id = Column(Integer, primary_key=True)

    source_phrase_id = Column(Integer, ForeignKey('phrases.id'))
    source_phrase = relationship('PhraseORM', back_populates='source_links', foreign_keys=[source_phrase_id])

    target_phrase_id = Column(Integer, ForeignKey('phrases.id'))
    target_phrase = relationship('PhraseORM', back_populates='target_links', foreign_keys=[target_phrase_id])

    study_phrases = relationship('StudyPhraseORM', back_populates='link')

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

    study_phrases = relationship('StudyPhraseORM', back_populates='account')


class StudyPhraseORM(Base):
    __tablename__ = 'study_phrases'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('AccountORM', back_populates='study_phrases')

    link_id = Column(Integer, ForeignKey('phrase_links.id'))
    link = relationship('PhraseLinkORM', back_populates='study_phrases')

    __table_args__ = (
        UniqueConstraint(
            'account_id',
            'link_id',
            name='account_link_unique',
        ),
    )
