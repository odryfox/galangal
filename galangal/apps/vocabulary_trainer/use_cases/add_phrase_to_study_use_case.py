from vocabulary_trainer.daos import PhraseToStudyDAO
from vocabulary_trainer.entities import PhraseToStudy


class AddPhraseToStudyUseCase:

    def __init__(self, phrase_to_study_dao: PhraseToStudyDAO):
        self._phrase_to_study_dao = phrase_to_study_dao

    def execute(self, phrase_to_study: PhraseToStudy, chat_id: str) -> None:
        self._phrase_to_study_dao.save_phrase(
            chat_id=chat_id,
            source_phrase=phrase_to_study.source_language_phrase,
            target_phrase=phrase_to_study.target_language_phrase,
        )


def create_add_phrase_to_study_use_case() -> AddPhraseToStudyUseCase:
    return AddPhraseToStudyUseCase(
        phrase_to_study_dao=PhraseToStudyDAO(),
    )
