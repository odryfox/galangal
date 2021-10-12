from typing import List, Optional

import bs4
import language.constants
import requests
from search_phrase_contexts.entities import PhraseContext


class PhraseContextsDAO:

    BASE_URL = 'https://context.reverso.net'

    LANGUAGES_MAP = {
        language.constants.Language.RU: 'russian',
        language.constants.Language.EN: 'english',
    }

    def _build_url(
        self,
        phrase: str,
        source_language: language.constants.Language,
        target_language: language.constants.Language,
    ) -> str:

        url_template = (
            '{base_url}/translation/'
            '{source_language}-{target_language}/{phrase}'
        )
        words = phrase.split()
        encoded_phrase = '+'.join(words)
        url = url_template.format(
            base_url=self.BASE_URL,
            source_language=self.LANGUAGES_MAP[source_language],
            target_language=self.LANGUAGES_MAP[target_language],
            phrase=encoded_phrase,
        )
        return url

    def _build_headers(self) -> dict:
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        return headers

    def search_phrase_contexts(
        self,
        phrase: str,
        source_language: language.constants.Language,
        target_language: language.constants.Language,
        limit: Optional[int] = None,
    ) -> List[PhraseContext]:

        url = self._build_url(
            phrase=phrase,
            source_language=source_language,
            target_language=target_language,
        )
        headers = self._build_headers()
        response = requests.get(url, headers=headers)
        html = response.text

        soup = bs4.BeautifulSoup(html, 'html.parser')
        examples = soup.findAll('div', {'class': 'example'})

        if limit is not None:
            examples = examples[:limit]

        phrase_contexts = []

        for example in examples:
            source = example.find(class_='src')
            source_language_phrase = example.find('em').text.strip()
            source_language_context = source.text.strip()

            target = example.find(class_='trg')
            target_language_phrase = target.find('a').text.strip()
            target_language_context = target.find(class_='text').text.strip()

            phrase_context = PhraseContext(
                source_language_phrase=source_language_phrase,
                source_language_context=source_language_context,
                target_language_phrase=target_language_phrase,
                target_language_context=target_language_context,
            )
            phrase_contexts.append(phrase_context)

        return phrase_contexts
