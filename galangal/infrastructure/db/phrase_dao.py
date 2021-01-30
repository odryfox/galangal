from domain.interfaces import IPhraseDAO
from infrastructure.db.models import (
    AccountORM,
    PhraseLinkORM,
    PhraseORM,
    StudyPhraseORM
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

        link_orm = self._session.query(PhraseLinkORM).filter_by(
            source_phrase_id=source_phrase_orm.id,
            target_phrase_id=target_phrase_orm.id,
        ).first()

        if not link_orm:
            link_orm = PhraseLinkORM(
                source_phrase_id=source_phrase_orm.id,
                target_phrase_id=target_phrase_orm.id,
            )
            self._session.add(link_orm)
            self._session.commit()

        account_orm = self._session.query(AccountORM).filter_by(
            telegram_chat_id=str(chat_id)
        ).first()
        if not account_orm:
            account_orm = AccountORM(telegram_chat_id=str(chat_id))
            self._session.add(account_orm)
            self._session.commit()

        study_phrase_orm = self._session.query(StudyPhraseORM).filter_by(
            account_id=account_orm.id, link_id=link_orm.id
        ).first()
        if not study_phrase_orm:
            study_phrase_orm = StudyPhraseORM(
                account_id=account_orm.id, link_id=link_orm.id
            )
            self._session.add(study_phrase_orm)
            self._session.commit()
