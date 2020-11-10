from unittest import mock

from domain.constants import Language
from domain.interfaces import PhraseUsage
from infrastructure.external import ReversoContextPhraseUsagesInDifferentLanguagesService


class TestReversoContextPhraseUsagesInDifferentLanguagesService:

    @classmethod
    def setup_class(cls):
        cls.service = ReversoContextPhraseUsagesInDifferentLanguagesService()

    def test_build_url(self):
        actual_url = self.service._build_url(
            phrase='I will be back',
            source_language=Language.EN,
            target_language=Language.RU,
        )

        expected_url = 'https://context.reverso.net/translation/' \
                       'english-russian/I+will+be+back'

        assert actual_url == expected_url

    def test_build_headers(self):
        actual_headers = self.service._build_header()

        assert 'User-Agent' in actual_headers
        assert 'python-requests' not in actual_headers['User-Agent']

    @mock.patch('galangal.infrastructure.external.requests.get')
    def test_search(self, mock_get):
        mock_get.return_value.text = """
        <div class="example">
          <div class="src ltr">
            <span class="text">If anyone should phone, say <em>I will be back</em> at one o'clock.</span>
          </div>
          <div class="trg ltr">
            <span class="icon jump-right"></span>
            <span class="text" lang="ru">Если кто-нибудь позвонит, скажи, что <a class="link_highlighted" href="/" ><em>я вернусь</em></a> в час.</span>
          </div>
        </div>
        <div class="example">
          <div class="src ltr">
            <span class="text"><em>I will be back</em> by 5, but just...</span>
          </div>
          <div class="trg ltr">
            <span class="icon jump-right"></span>
            <span class="text" lang="ru"><a class="link_highlighted" href="/" ><em>Я вернусь</em></a> к пяти, но если...</span>
          </div>
        </div>
        """

        actual_result = self.service.search(
            phrase='I will be back',
            source_language=Language.EN,
            target_languages=[Language.RU],
            limit=5,
        )

        url = self.service._build_url(
            phrase='I will be back',
            source_language=Language.EN,
            target_language=Language.RU,
        )
        headers = self.service._build_header()

        mock_get.assert_called_once_with(url, headers=headers)

        expected_result = [
            {
                Language.EN: PhraseUsage(
                    text="If anyone should phone, say I will be back at one o'clock.",
                    phrase='I will be back',
                ),
                Language.RU: PhraseUsage(
                    text='Если кто-нибудь позвонит, скажи, что я вернусь в час.',
                    phrase='я вернусь',
                ),
            },
            {
                Language.EN: PhraseUsage(
                    text='I will be back by 5, but just...',
                    phrase='I will be back',
                ),
                Language.RU: PhraseUsage(
                    text='Я вернусь к пяти, но если...',
                    phrase='Я вернусь',
                ),
            },
        ]

        assert actual_result == expected_result
