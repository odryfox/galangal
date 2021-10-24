from typing import Union

import bot.constants
from bot.markdown import Action, MarkdownActionComponent, MarkdownDocument
from millet import BaseSkill
from search_phrase_contexts.use_cases import (
    SearchPhraseContextsUseCase,
    create_search_phrase_contexts_use_case
)
from vocabulary_trainer.use_cases import (
    create_suggest_phrases_to_study_use_case
)


class SearchPhraseContextsSkill(BaseSkill):

    def execute(self, message: str, user_id: str) -> Union[str, MarkdownDocument]:
        search_phrase_contexts_use_case = create_search_phrase_contexts_use_case()

        try:
            phrase_contexts = (
                search_phrase_contexts_use_case.execute(phrase=message)
            )
        except SearchPhraseContextsUseCase.MultilingualException:
            return 'Фраза должна быть на русском или английском языке'
        except SearchPhraseContextsUseCase.NonSpecificLanguageException:
            return 'Это легко) Фраза так и переводится: {}'.format(message)

        if not phrase_contexts:
            return 'К сожалению я ничего не нашел'.format(message)

        text_components = [
            '{}\n{}\n\n'.format(
                phrase_context.source_language_context,
                phrase_context.target_language_context,
            )
            for phrase_context in phrase_contexts
        ]

        suggest_phrases_to_study_use_case = create_suggest_phrases_to_study_use_case()

        phrases_to_study = (
            suggest_phrases_to_study_use_case.execute(
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
        return response
