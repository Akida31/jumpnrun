from enum import Enum


class Language(Enum):
    DE = ("DE",)
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
        if translation := translations[self.language.name].get(text):
            return translation
        # return the input back
        return text


# create a global translator
t = Translator()

translations = {
    "EN": {
        "hint1": 'Press "a" to move left and "d" to move right.\nCollect the coin!',
        "hint2": 'You can jump with "w"!',
    },
    "DE": {
        "Quit Game": "Spiel beenden",
        "Continue": "Fortfahren",
        "Play": "Spielen",
        "About Game": "Über das Spiel",
        "Restart Level": "Level neustarten",
        "Completed Level #x in #ts": "Level #x in #ts beendet",
        "Back to Title Screen": "Zurück zum Hauptmenü",
        "Time": "Zeit",
        "Next Level": "Nächstes Level",
        "hint1": 'Drücke "a" um dich nach links zu bewegen\nund "d" um dich nach rechts zu bewegen.\nSammle die Münze!',
        "hint2": 'Du kannst mit "w" springen!',
    },
}
