from skyjump.config import MUTED, SOUND_VOLUME, DATA_DIR
import time
import pygame
from os import path
from threading import Thread


def play_sound(sound_file: str, pause: bool = False):
    """
    play the sound file if the volume is on
    """
    if MUTED:
        return
    if pause:
        pygame.mixer.music.pause()
    sound = pygame.mixer.Sound(path.join(DATA_DIR, "sounds", sound_file))
    sound.set_volume(SOUND_VOLUME)
    sound.play()
    if pause:
        length = sound.get_length()
        # delay the unpausing
        # a thread is necessary because else the full game would sleep
        Thread(target=_unpause_music, args=[length], daemon=True).start()


def _unpause_music(waiting_time: float):
    time.sleep(waiting_time)
    # unpause the music if it isn't playing
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
