import pytest
from _pytest.fixtures import FixtureRequest
from infrastructure.db.models import AccountORM
from infrastructure.db.phrase_dao import DBPhraseDAO
from sqlalchemy.orm import Session


class TestPhraseDAO:

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, request: FixtureRequest, session: Session):
        self.session = session
        self.dao = DBPhraseDAO(session=self.session)
        self.chat_id = '100500'

    def test(self):
        self.dao.save_phrase(
            chat_id=self.chat_id,
            source_phrase='hello',
            target_phrase='привет',
        )

        account_orm = self.session.query(AccountORM).filter_by(
            telegram_chat_id=self.chat_id,
        ).first()

        assert account_orm.telegram_chat_id == self.chat_id
