from search_phrase_contexts.entities import PhraseContext
from vocabulary_trainer.entities import PhraseToStudy
from vocabulary_trainer.use_cases import SuggestPhrasesToStudyUseCase


class TestSuggestPhrasesToStudyUseCase:

    def setup_method(self):
        self.use_case = SuggestPhrasesToStudyUseCase()

    def test_execute(self):
        phrase_contexts = [
            PhraseContext(
                source_language_phrase='one',
                source_language_context='context',
                target_language_phrase='один',
                target_language_context='context',
            ),
            PhraseContext(
                source_language_phrase='two',
                source_language_context='context',
                target_language_phrase='два',
                target_language_context='context',
            ),
            PhraseContext(
                source_language_phrase='One',
                source_language_context='context',
                target_language_phrase='Один',
                target_language_context='context',
            ),
        ]

        suggestions_phrases_to_study_actual = self.use_case.execute(
            phrase_contexts=phrase_contexts,
        )

        suggestions_phrases_to_study_expected = [
            PhraseToStudy(
                source_language_phrase='one',
                target_language_phrase='один',
            ),
            PhraseToStudy(
                source_language_phrase='two',
                target_language_phrase='два',
            ),
        ]
        assert (
            suggestions_phrases_to_study_actual ==
            suggestions_phrases_to_study_expected
        )
