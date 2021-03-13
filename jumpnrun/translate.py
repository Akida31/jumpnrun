from enum import Enum
from typing import Dict
from json import load
from jumpnrun import config
from os import path


class Language(Enum):
    DE = "DE"
    EN = "EN"


class Translator:
    """
    basic translation class
    """

    def __init__(self, language: Language = Language.EN):
        """
        create a translator
        """
        self.language = language
        self.translations = load_translations()

    def change_language(self, language: Language):
        """
        change the language of the translator
        """
        self.language = language

    def __call__(self, text: str) -> str:
        """
        translate the given text

        Wrapper of `translate`
        """
        return self.translate(text)

    def translate(self, text: str) -> str:
        """
        translate the given text
        """
        # return the translation if there is one
        if translation := self.translations[self.language.name].get(text):
            return translation
        # return the input back
        return text


def load_translations() -> Dict:
    """
    load the translations from its json file
    """
    with open(path.join(config.DATA_DIR, "translations.json")) as f:
        return load(f)


# create a global translator
t = Translator()
