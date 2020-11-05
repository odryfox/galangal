from unittest import mock

from galangal.domain.constants import LanguageEnum
from galangal.domain.entities import UsageCollocation
from galangal.infrasructure.external import \
    ReversoContextUsageCollocationsService


class TestReversoContextUsageCollocationsServiceTestCase:

    @classmethod
    def setup_class(cls):
        cls.service = ReversoContextUsageCollocationsService()

    def test_build_url(self):
        actual_url = self.service._build_url(
            collocation='I will be back',
            source_language=LanguageEnum.EN,
            target_language=LanguageEnum.RU,
        )

        expected_url = 'https://context.reverso.net/translation/' \
                       'english-russian/I+will+be+back'

        assert actual_url == expected_url

    def test_build_headers(self):
        actual_headers = self.service._build_header()

        assert 'User-Agent' in actual_headers
        assert 'python-requests' not in actual_headers['User-Agent']

    @mock.patch('galangal.infrasructure.external.requests.get')
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
            collocation='I will be back',
            source_language=LanguageEnum.EN,
            target_language=LanguageEnum.RU,
        )

        url = self.service._build_url(
            collocation='I will be back',
            source_language=LanguageEnum.EN,
            target_language=LanguageEnum.RU,
        )
        headers = self.service._build_header()

        mock_get.assert_called_once_with(url, headers=headers)

        expected_result = [
            {
                LanguageEnum.EN: UsageCollocation(
                    sentence="If anyone should phone, say I will be back at one o'clock.",
                    collocation_from_sentence='I will be back',
                ),
                LanguageEnum.RU: UsageCollocation(
                    sentence='Если кто-нибудь позвонит, скажи, что я вернусь в час.',
                    collocation_from_sentence='я вернусь',
                ),
            },
            {
                LanguageEnum.EN: UsageCollocation(
                    sentence='I will be back by 5, but just...',
                    collocation_from_sentence='I will be back',
                ),
                LanguageEnum.RU: UsageCollocation(
                    sentence='Я вернусь к пяти, но если...',
                    collocation_from_sentence='Я вернусь',
                ),
            },
        ]

        assert actual_result == expected_result
