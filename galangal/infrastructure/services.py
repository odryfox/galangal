import re

from domain.constants import Language
from domain.interfaces import ILanguageService


class RegexLanguageService(ILanguageService):

    def get_language(self, text: str) -> Language:
        if bool(re.search('[а-яА-Я]', text)):
            return Language.RU
        else:
            return Language.EN
