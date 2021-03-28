import random
from typing import Optional

from domain.entities import PhraseToStudy
from domain.interfaces import IPhraseDAO
from infrastructure.db.models import (
    AccountORM,
    PhraseORM,
    StudySynonymORM,
    SynonymORM
)
from sqlalchemy.orm import Session


class DBPhraseDAO(IPhraseDAO):

    def __init__(self, session: Session):
        self._session = session

    def save_phrase(
        self,
        chat_id: str,
        source_phrase: str,
        target_phrase: str
    ) -> None:

        source_phrase_orm = self._session.query(PhraseORM).filter_by(
            value=source_phrase
        ).first()

        if not source_phrase_orm:
            source_phrase_orm = PhraseORM(value=source_phrase)
            self._session.add(source_phrase_orm)
            self._session.commit()

        target_phrase_orm = self._session.query(PhraseORM).filter_by(
            value=target_phrase
        ).first()

        if not target_phrase_orm:
            target_phrase_orm = PhraseORM(value=target_phrase)
            self._session.add(target_phrase_orm)
            self._session.commit()

        synonym_orm = self._session.query(SynonymORM).filter_by(
            source_phrase_id=source_phrase_orm.id,
            target_phrase_id=target_phrase_orm.id,
        ).first()

        if not synonym_orm:
            synonym_orm = SynonymORM(
                source_phrase_id=source_phrase_orm.id,
                target_phrase_id=target_phrase_orm.id,
            )
            self._session.add(synonym_orm)
            self._session.commit()

        account_orm = self._session.query(AccountORM).filter_by(
            telegram_chat_id=str(chat_id)
        ).first()
        if not account_orm:
            account_orm = AccountORM(telegram_chat_id=str(chat_id))
            self._session.add(account_orm)
            self._session.commit()

        study_synonym_orm = self._session.query(StudySynonymORM).filter_by(
            account_id=account_orm.id, synonym_id=synonym_orm.id
        ).first()
        if not study_synonym_orm:
            study_phrase_orm = StudySynonymORM(
                account_id=account_orm.id, synonym_id=synonym_orm.id
            )
            self._session.add(study_phrase_orm)
            self._session.commit()

    def get_phrase(self, chat_id: str) -> Optional[PhraseToStudy]:
        try:
            account_orm = self._session.query(AccountORM).filter_by(
                telegram_chat_id=str(chat_id)
            ).first()

            query = self._session.query(StudySynonymORM).filter_by(account_id=account_orm.id)
            random_index = random.randrange(0, query.count())
            study_synonym_orm = query[random_index]

            synonym_orm = self._session.query(SynonymORM).get(study_synonym_orm.synonym_id)
        except:
            return None
        return PhraseToStudy(
            source_phrase=synonym_orm.source_phrase.value,
            target_phrase=synonym_orm.target_phrase.value,
        )
