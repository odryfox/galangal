from typing import List

from domain.entities import PhraseToStudy, PhraseUsagesInDifferentLanguages


class GetPhraseToStudyFromSearchUsecase:

    def execute(self, phrase_usages_in_different_languages: PhraseUsagesInDifferentLanguages) -> List[PhraseToStudy]:
        languages = list(phrase_usages_in_different_languages[0].keys())

        source_language = languages[0]
        target_language = languages[1]

        phrases = set()
        for phrase_usage_in_different_languages in phrase_usages_in_different_languages:
            phrase_in_source_language = phrase_usage_in_different_languages[source_language].phrase.lower()
            phrase_in_target_language = phrase_usage_in_different_languages[target_language].phrase.lower()

            phrases.add((phrase_in_source_language, phrase_in_target_language))

        phrases_to_study = []
        for phrase in phrases:
            phrase_in_source_language = phrase[0]
            phrase_in_target_language = phrase[1]

            phrases_to_study.append(
                PhraseToStudy(
                    source_phrase=phrase_in_source_language,
                    target_phrase=phrase_in_target_language
                )
            )

        return phrases_to_study
