from enum import Enum
from typing import Dict
from json import load
from skyjump import config
from os import path


class Language(Enum):
    """Languages to which can be translated"""

    DE = "DE"
    EN = "EN"


class Translator:
    """translator for the game

    usage:
    ```
    translator = Translator() # create a translator
    translator("Hello World")  # translate Hello World
    ```
    """

    def __init__(self, language: Language = Language.EN):
        """create a translator

        :param language: the language to which should be translated
        """
        self.language = language
        self.translations = load_translations()

    def change_language(self, language: Language):
        """change the language of the translator"""
        self.language = language

    def __call__(self, text: str) -> str:
        """translate the given text

        Wrapper of `translate`
        """
        return self.translate(text)

    def translate(self, text: str) -> str:
        """translate to other languages

        :param text: text which should be translated
        :returns: the translated text
        """
        # return the translation if there is one
        if translation := self.translations[self.language.name].get(text):
            return translation
        # return the input back
        return text


def load_translations() -> Dict:
    """load the translations from its json file"""
    with open(path.join(config.DATA_DIR, "translations.json")) as f:
        return load(f)


# create a global translator
t = Translator()
