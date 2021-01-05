from domain.interfaces import IPhraseDAO


class SavePhraseToStudyUsecase:

    def __init__(self, phrase_dao: IPhraseDAO):
        self._phrase_dao = phrase_dao

    def execute(self, chat_id: str, source_phrase: str, target_phrase: str):
        self._phrase_dao.save_phrase(
            chat_id=chat_id,
            source_phrase=source_phrase,
            target_phrase=target_phrase,
        )
