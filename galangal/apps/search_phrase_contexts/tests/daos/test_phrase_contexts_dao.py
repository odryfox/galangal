from unittest import mock

from language.constants import Language
from search_phrase_contexts.daos import PhraseContextsDAO
from search_phrase_contexts.entities import PhraseContext


class TestPhraseContextsDAO:

    def setup_method(self):
        self.dao = PhraseContextsDAO()

    @mock.patch('search_phrase_contexts.daos.phrase_contexts_dao.requests.get')
    def test_search_phrase_contexts(self, mock_get):
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

        phrase_contexts_actual = self.dao.search_phrase_contexts(
            phrase='I will be back',
            source_language=Language.EN,
            target_language=Language.RU,
            limit=5,
        )

        phrase_contexts_expected = [
            PhraseContext(
                source_language_phrase='I will be back',
                source_language_context='If anyone should phone, say I will be back at one o\'clock.',
                target_language_phrase='я вернусь',
                target_language_context='Если кто-нибудь позвонит, скажи, что я вернусь в час.',
            ),
            PhraseContext(
                source_language_phrase='I will be back',
                source_language_context='I will be back by 5, but just...',
                target_language_phrase='Я вернусь',
                target_language_context='Я вернусь к пяти, но если...',
            ),
        ]
        assert phrase_contexts_actual == phrase_contexts_expected

        url_expected = 'https://context.reverso.net/translation/' \
                       'english-russian/I+will+be+back'
        headers_expected = {'User-Agent': 'Mozilla/5.0'}
        mock_get.assert_called_once_with(url_expected, headers=headers_expected)
