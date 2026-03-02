import os
import time
import pygame
from .states import MusicStates, StateHandler
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self, folder):
        self.folder = folder
        self.music_files = []
        self.current_position = 0.0
        self.play_start_time = None  # wall clock time when play() was last called
        self.current_song = None
        self.state_handler = StateHandler()

        try:
            pygame.mixer.init()
        except pygame.error as e:
            print('error initializing!', e)

        self._load_files()

    def _load_files(self):
        if not os.path.isdir(self.folder):
            print(f" folder '{self.folder}' not found!")
            return
        self.music_files = [
            f for f in os.listdir(self.folder) if f.endswith('.mp3')
        ]  # checks if the files are mp3
    def get_position(self):
        if self.state_handler.state == MusicStates.PLAYING:
            return self.current_position + (time.time() - self.play_start_time)
        return self.current_position

    # controls
    def load(self, music_file_name): # load specific music
        music_path = os.path.join(self.folder, music_file_name)
        pygame.mixer.music.load(music_path)

        self.current_song = music_file_name
        self.current_position = 0.0
        self.play_start_time = None
        #self.state_handler.change_state(MusicStates.LOADED)
    def get_song_length(self, music_file_name):
        music_path = os.path.join(self.folder, music_file_name)
        audio = MP3(music_path)
        return audio.info.length
    def play(self, position=None): # play the loaded music
        if position is not None:
            self.current_position = position
        pygame.mixer.music.play(start=self.current_position)
        self.play_start_time = time.time()
        self.state_handler.change_state(MusicStates.PLAYING)

    def pause(self):
        if self.state_handler.is_state(MusicStates.PLAYING):
            pygame.mixer.music.pause()
            self.current_position = self.get_position()  # freeze at current moment
            self.play_start_time = None
            self.state_handler.change_state(MusicStates.PAUSED)

    def resume(self):
        if self.state_handler.is_state(MusicStates.PAUSED):
            pygame.mixer.music.unpause()
            self.play_start_time = time.time()  # reset
            self.state_handler.change_state(MusicStates.PLAYING)

    def stop(self):
        pygame.mixer.music.stop()
        self.current_song = None
        self.current_position = 0.0
        self.play_start_time = None
        self.state_handler.change_state(MusicStates.STOPPED)

    def go_back(self, seconds=5):
        # Go back 5 seconds
        if self.state_handler.is_state(MusicStates.PLAYING) or self.state_handler.is_state(MusicStates.PAUSED):
            self.play(max(0, self.get_position() - seconds))  # max() to avoid negative numbers

    def go_forward(self, seconds=5):
        # Go forward 5 seconds
        if self.state_handler.is_state(MusicStates.PLAYING) or self.state_handler.is_state(MusicStates.PAUSED):
            self.play(min(self.get_song_length(self.current_song),self.get_position() + seconds))

    def set_volume(self, volume: float):
        if self.state_handler.is_state(MusicStates.PLAYING):
            pygame.mixer.music.set_volume(volume)
    def get_busy(self):
        return pygame.mixer.music.get_busy()