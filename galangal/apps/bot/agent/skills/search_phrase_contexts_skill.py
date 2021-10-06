import bot.constants
from bot.markdown import Action, MarkdownActionComponent, MarkdownDocument
from millet import BaseSkill
from search_phrase_contexts.use_cases import SearchPhraseContextsUseCase
from vocabulary_trainer.use_cases import SuggestPhrasesToStudyUseCase


class SearchPhraseContextsSkill(BaseSkill):

    def __init__(
        self,
        search_phrase_contexts_use_case: SearchPhraseContextsUseCase,
        suggest_phrases_to_study_use_case: SuggestPhrasesToStudyUseCase,
    ) -> None:
        self.search_phrase_contexts_use_case = search_phrase_contexts_use_case
        self.suggest_phrases_to_study_use_case = suggest_phrases_to_study_use_case

    def execute(self, message: str):
        try:
            phrase_contexts = (
                self.search_phrase_contexts_use_case.execute(phrase=message)
            )
        except SearchPhraseContextsUseCase.MultilingualException:
            self.say('Фраза должна быть на русском или английском языке')
            return
        except SearchPhraseContextsUseCase.NonSpecificLanguageException:
            self.say('Это легко) Фраза так и переводится: {}'.format(message))
            return

        if not phrase_contexts:
            self.say('К сожалению я ничего не нашел'.format(message))
            return

        text_components = [
            '{}\n{}\n\n'.format(
                phrase_context.source_language_context,
                phrase_context.target_language_context,
            )
            for phrase_context in phrase_contexts
        ]

        phrases_to_study = (
            self.suggest_phrases_to_study_use_case.execute(
                phrase_contexts=phrase_contexts,
            )
        )
        add_phrases_to_study_action_components = [
            MarkdownActionComponent(
                text='+ {} - {}'.format(
                    phrase_to_study.source_language_phrase,
                    phrase_to_study.target_language_phrase,
                ),
                action=Action(
                    action_type=bot.constants.ActionType.ADD_PHRASE_TO_STUDY,
                    params={
                        'source_language_phrase': phrase_to_study.source_language_phrase,
                        'target_language_phrase': phrase_to_study.target_language_phrase,
                    },
                ),
            )
            for phrase_to_study in phrases_to_study
        ]

        response = MarkdownDocument(
            components=text_components + add_phrases_to_study_action_components,
        )
        self.say(response)
