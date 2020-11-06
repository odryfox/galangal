from typing import Dict, List, Optional

import bs4
import requests

from domain.constants import LanguageEnum
from domain.entities import UsageCollocation
from domain.interfaces import IUsageCollocationsService


class ReversoContextUsageCollocationsService(IUsageCollocationsService):

    BASE_URL = 'https://context.reverso.net'

    LANGUAGE_MAP = {
        LanguageEnum.RU: 'russian',
        LanguageEnum.EN: 'english',
    }

    def _build_url(
        self,
        collocation: str,
        source_language: LanguageEnum,
        target_language: LanguageEnum,
    ) -> str:
        url_template = '{base_url}/translation/' \
                       '{source_language}-{target_language}/{collocation}'
        words = collocation.split()
        encoded_collocation = '+'.join(words)
        url = url_template.format(
            base_url=self.BASE_URL,
            source_language=self.LANGUAGE_MAP[source_language],
            target_language=self.LANGUAGE_MAP[target_language],
            collocation=encoded_collocation,
        )
        return url

    def _build_header(self) -> dict:
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        return headers

    def search(
        self,
        collocation: str,
        source_language: LanguageEnum,
        target_language: LanguageEnum,
        limit: Optional[int] = None,
    ) -> List[Dict[LanguageEnum, UsageCollocation]]:

        url = self._build_url(
            collocation=collocation,
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

        result = []

        for example in examples:
            source = example.find(class_='src')
            source_sentence = source.text.strip()
            source_collocation_from_sentence = example.find('em').text.strip()

            usage_collocation_in_source_language = UsageCollocation(
                sentence=source_sentence,
                collocation_from_sentence=source_collocation_from_sentence,
            )

            target = example.find(class_='trg')
            target_sentence = target.find(class_='text').text.strip()
            target_collocation_from_sentence = target.find('a').text.strip()

            usage_collocation_in_target_language = UsageCollocation(
                sentence=target_sentence,
                collocation_from_sentence=target_collocation_from_sentence,
            )

            result.append(
                {
                    source_language: usage_collocation_in_source_language,
                    target_language: usage_collocation_in_target_language,
                }
            )

        return result
