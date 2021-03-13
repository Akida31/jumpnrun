import os

# the directory of the assets
DATA_DIR: str = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "assets")
)

from jumpnrun import translate

# the language of the game
LANGUAGE: translate.Language = translate.Language.DE

# if the game has sound or is muted
MUTED: bool = False

# the volume of the sounds
# 0.0 is minimal and 1.0 is maximal
SOUND_VOLUME: float = 0.3

# the volume of the music
# 0.0 is minimal and 1.0 is maximal
MUSIC_VOLUME: float = 0.5
