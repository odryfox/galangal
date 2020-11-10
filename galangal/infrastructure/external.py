from typing import List

import bs4
import requests

from domain.constants import Language
from domain.interfaces import PhraseUsagesInDifferentLanguages, PhraseUsage
from domain.interfaces import IPhraseUsagesInDifferentLanguagesService


class ReversoContextPhraseUsagesInDifferentLanguagesService(IPhraseUsagesInDifferentLanguagesService):

    BASE_URL = 'https://context.reverso.net'

    LANGUAGE_MAP = {
        Language.RU: 'russian',
        Language.EN: 'english',
    }

    def _build_url(
        self,
        phrase: str,
        source_language: Language,
        target_language: Language,
    ) -> str:

        url_template = '{base_url}/translation/' \
                       '{source_language}-{target_language}/{phrase}'
        words = phrase.split()
        encoded_phrase = '+'.join(words)
        url = url_template.format(
            base_url=self.BASE_URL,
            source_language=self.LANGUAGE_MAP[source_language],
            target_language=self.LANGUAGE_MAP[target_language],
            phrase=encoded_phrase,
        )
        return url

    def _build_header(self) -> dict:
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        return headers

    def search(
        self,
        phrase: str,
        source_language: Language,
        target_languages: List[Language],
        limit: int,
    ) -> PhraseUsagesInDifferentLanguages:

        target_language = target_languages[0]

        url = self._build_url(
            phrase=phrase,
            source_language=source_language,
            target_language=target_language,
        )
        headers = self._build_header()
        response = requests.get(url, headers=headers)
        html = response.text

        soup = bs4.BeautifulSoup(html)
        examples = soup.findAll('div', {'class': 'example'})
        if limit is not None:
            examples = examples[:limit]

        phrase_usages_in_different_languages = []

        for example in examples:
            source = example.find(class_='src')
            text_in_source_language = source.text.strip()
            phrase_in_source_language = example.find('em').text.strip()

            phrase_usage_in_source_language = PhraseUsage(
                text=text_in_source_language,
                phrase=phrase_in_source_language,
            )

            target = example.find(class_='trg')
            text_in_target_language = target.find(class_='text').text.strip()
            phrase_in_target_language = target.find('a').text.strip()

            phrase_usage_in_target_language = PhraseUsage(
                text=text_in_target_language,
                phrase=phrase_in_target_language,
            )

            phrase_usages_in_different_languages.append(
                {
                    source_language: phrase_usage_in_source_language,
                    target_language: phrase_usage_in_target_language,
                }
            )

        return phrase_usages_in_different_languages
