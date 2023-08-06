import logging
import time
from multiprocessing import Process, Value

import pygame

from smb3_eh_manip import settings
from smb3_eh_manip.settings import ACTION_FRAMES, FREQUENCY

DEFAULT_AUDIO_CUE_PATH = "data/audio_cue.wav"
AUDIO_CUE_PATH = settings.get("audio_cue_path", fallback=DEFAULT_AUDIO_CUE_PATH)


def play_audio_cue(play):
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_CUE_PATH)
    while True:
        play_sound = False
        with play.get_lock():
            if play.value == 1:
                play.value = 0
                play_sound = True
        if play_sound:
            pygame.mixer.music.play()
        else:
            time.sleep(0.001)


class AudioPlayer:
    def __init__(self):
        self.play = Value("i", 0)
        self.play_process = Process(target=play_audio_cue, args=(self.play,)).start()

    def reset(self):
        self.play.value = 0
        self.trigger_frames = []
        for action_frame in ACTION_FRAMES:
            for increment in range(4, -1, -1):
                self.trigger_frames.append(action_frame - increment * FREQUENCY)
        logging.info(f"Audio trigger frames set to {self.trigger_frames}")

    def tick(self, current_frame):
        if self.trigger_frames and self.trigger_frames[0] <= current_frame:
            self.trigger_frames.pop(0)
            with self.play.get_lock():
                self.play.value = 1
