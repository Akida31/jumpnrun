from skyjump.config import MUTED, SOUND_VOLUME, DATA_DIR
import time
import pygame
from os import path
from threading import Thread


def play_sound(sound_file: str, pause: bool = False):
    """play the sound file if the volume is on

    :param sound_file: the file of the sound
    :param pause: if the music should be paused
    """
    # if muted, do nothing
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
    """unpauser of the music after sound has ended
    :param waiting_time: the time to wait before unpausing
    """
    time.sleep(waiting_time)
    # unpause the music if it isn't playing
    # without the check the program will quit sometimes after delay
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
