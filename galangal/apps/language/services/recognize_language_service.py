import string

import language.constants


class RecognizeLanguageService:

    ALPHABET_EN = set(string.ascii_lowercase)
    ALPHABET_RU = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

    class MultilingualException(Exception):
        pass

    class NonSpecificLanguageException(Exception):
        pass

    def execute(self, text: str) -> language.constants.Language:
        is_english = False
        is_russian = False

        for latter in text.lower():
            if latter in self.ALPHABET_EN:
                is_english = True
            elif latter in self.ALPHABET_RU:
                is_russian = True

            if is_english and is_russian:
                raise self.MultilingualException

        if is_english:
            return language.constants.Language.EN
        elif is_russian:
            return language.constants.Language.RU
        else:
            raise self.NonSpecificLanguageException
