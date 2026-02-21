import os
import time
import pygame
from mutagen.mp3 import MP3

# will potentially be modified further

class MusicPlayer:
    def __init__(self, folder):
        self.folder = folder
        self.music_files = []
        self.current_position = 0.0
        self.play_start_time = None  # wall clock time when play() was last called
        self.is_paused = False
        self.is_playing = False
        self.current_song = None

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
        if not self.is_playing or self.is_paused or self.play_start_time is None:
            return self.current_position
        return self.current_position + (time.time() - self.play_start_time)

    # controls
    def load(self, music_file_name): # load specific music
        music_path = os.path.join(self.folder, music_file_name)
        pygame.mixer.music.load(music_path)

        self.current_song = music_file_name
        self.current_position = 0.0
        self.play_start_time = None
        self.is_paused = False
        self.is_playing = False

    def get_song_length(self, music_file_name):
        music_path = os.path.join(self.folder, music_file_name)
        audio = MP3(music_path)
        return audio.info.length
    def play(self, position=None): # play the loaded music
        if position is not None:
            self.current_position = position
        pygame.mixer.music.play(start=self.current_position)
        self.play_start_time = time.time()
        self.is_playing = True
        self.is_paused = False

    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.current_position = self.get_position()  # freeze at current moment
            self.play_start_time = None
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.play_start_time = time.time()  # reset
            self.is_paused = False

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
        self.current_song = None
        self.current_position = 0.0
        self.play_start_time = None
        self.is_playing = False
        self.is_paused = False

    def go_back(self, seconds=5):
        # Go back 5 seconds
        if self.is_playing:
            self.play(max(0, self.get_position() - seconds))  # max() to avoid negative numbers

    def go_forward(self, seconds=25):
        # Go forward 5 seconds
        if self.is_playing:
            self.play(min(self.get_song_length(self.current_song),self.get_position() + seconds))

    def set_volume(self, volume: float):
        if self.is_playing:
            pygame.mixer.music.set_volume(volume)
    def get_busy(self):
        return pygame.mixer.music.get_busy()