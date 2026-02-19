import os
import pygame
import time
"""
used for warmup. training with pygame music. will be enhanced with gui and
the desktop app will be connected to mobile device, which will serve as a remote
"""

# ── GUI layer ─────────────────────────────────────────────────────────────────
import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QSlider, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor, QPalette
# ─────────────────────────────────────────────────────────────────────────────


def play_music(folder, music_file_name):
    music_path = os.path.join(folder, music_file_name)
    pygame.mixer.music.load(music_path)

    current_position = 0.0
    last_update_time = time.time() # some arbitrary num

    pygame.mixer.music.play(start=current_position)

    while True:
        if not pygame.mixer.music.get_busy(): # only update if it's playing
            current_position += time.time() - last_update_time #time.time is updated now and we subtract last updated time to get the difference
            # the difference indicates how much time has passed since the song has started
        last_update_time = time.time() # update

        print("P - pause; R - Resume; S - stop; D - +5 seconds; A - -5 seconds")
        user_input = input('-> ')

        match user_input.lower().strip():
            case 'p':
                pygame.mixer.music.pause()

            case 'r':
                pygame.mixer.music.unpause()
                last_update_time = time.time() # update again

            case 's':
                pygame.mixer.music.stop()
                break

            case 'a':
                current_position = max(0, current_position - 5) # max() to avoid negative numbers
                pygame.mixer.music.play(start=current_position)
                last_update_time = time.time()

            case 'd':
                current_position += 5
                pygame.mixer.music.play(start=current_position)
                last_update_time = time.time()

            case _:
                print('Invalid input')


# ── GUI classes ───────────────────────────────────────────────────────────────
class PlayerState(QObject):
    """Holds shared playback state so the GUI can read/write it thread-safely."""
    song_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_position = 0.0
        self.last_update_time = time.time()
        self.is_paused = False
        self.is_playing = False
        self.lock = threading.Lock()


class MusicPlayerWindow(QMainWindow):
    SONGS_FOLDER = "songs"

    def __init__(self):
        super().__init__()
        self.state = PlayerState()
        self.music_files = []
        self._setup_pygame()
        self._load_songs()
        self._build_ui()
        self._start_tick()

    # ── init helpers ──────────────────────────────────────────────────────────
    def _setup_pygame(self):
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print('error initializing!', e)

    def _load_songs(self):
        if not os.path.isdir(self.SONGS_FOLDER):
            print(f" folder '{self.SONGS_FOLDER}' not found!")
            return
        self.music_files = [
            f for f in os.listdir(self.SONGS_FOLDER) if f.endswith('.mp3')
        ] # checks if the files are mp3 then adds

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        self.setWindowTitle("🎵 Music App")
        self.setMinimumSize(520, 620)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0f0f0f;
                color: #e8e8e8;
            }
            QListWidget {
                background-color: #181818;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 4px;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 10px 14px;
                border-radius: 6px;
                color: #b0b0b0;
            }
            QListWidget::item:selected {
                background-color: #1db954;
                color: #000000;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: #252525;
                color: #e8e8e8;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #e8e8e8;
                border: 1px solid #333;
                border-radius: 22px;
                font-size: 18px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #1db954;
                color: #000;
                border-color: #1db954;
            }
            QPushButton:pressed {
                background-color: #17a349;
            }
            QPushButton#playBtn {
                background-color: #1db954;
                color: #000;
                border: none;
                font-size: 22px;
                border-radius: 26px;
            }
            QPushButton#playBtn:hover { background-color: #1ed760; }
            QSlider::groove:horizontal {
                height: 4px;
                background: #333;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #1db954;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #fff;
                width: 12px; height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QLabel { background: transparent; }
        """)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ── header ────────────────────────────────────────────────────────────
        header = QLabel("MUSIC APP")
        header.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        header.setStyleSheet("color: #1db954; letter-spacing: 4px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # ── now playing ───────────────────────────────────────────────────────
        self.now_playing = QLabel("No song selected")
        self.now_playing.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.now_playing.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.now_playing.setWordWrap(True)
        self.now_playing.setStyleSheet("color: #fff; padding: 8px 0;")
        layout.addWidget(self.now_playing)

        # ── time bar ──────────────────────────────────────────────────────────
        time_row = QHBoxLayout()
        self.time_elapsed = QLabel("0:00")
        self.time_elapsed.setStyleSheet("color: #777; font-size: 11px;")
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 1000)
        self.seek_slider.sliderMoved.connect(self._on_seek)
        self.time_total = QLabel("0:00")
        self.time_total.setStyleSheet("color: #777; font-size: 11px;")
        time_row.addWidget(self.time_elapsed)
        time_row.addWidget(self.seek_slider)
        time_row.addWidget(self.time_total)
        layout.addLayout(time_row)

        # ── controls ──────────────────────────────────────────────────────────
        controls = QHBoxLayout()
        controls.setSpacing(10)
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_back   = self._ctrl_btn("⏮", self._prev_song)
        self.btn_rewind = self._ctrl_btn("«", self._rewind)        # A: -5s
        self.btn_play   = self._ctrl_btn("▶", self._toggle_play, obj_name="playBtn", size=52)
        self.btn_fwd    = self._ctrl_btn("»", self._forward)       # D: +5s
        self.btn_next   = self._ctrl_btn("⏭", self._next_song)
        self.btn_stop   = self._ctrl_btn("■", self._stop)

        for btn in (self.btn_back, self.btn_rewind, self.btn_play,
                    self.btn_fwd, self.btn_next, self.btn_stop):
            controls.addWidget(btn)

        layout.addLayout(controls)

        # ── divider ───────────────────────────────────────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #2a2a2a;")
        layout.addWidget(line)

        # ── song list ─────────────────────────────────────────────────────────
        list_label = QLabel("Library")
        list_label.setFont(QFont("Segoe UI", 10))
        list_label.setStyleSheet("color: #777; letter-spacing: 1px;")
        layout.addWidget(list_label)

        self.song_list = QListWidget()
        self.song_list.itemDoubleClicked.connect(self._on_double_click)
        for f in self.music_files:
            self.song_list.addItem(QListWidgetItem(f.strip(".mp3")))
        layout.addWidget(self.song_list)

        self.current_index = -1

    def _ctrl_btn(self, text, slot, obj_name=None, size=44):
        btn = QPushButton(text)
        btn.setFixedSize(size, size)
        if obj_name:
            btn.setObjectName(obj_name)
        btn.clicked.connect(slot)
        return btn

    # ── tick timer (updates slider + elapsed time) ────────────────────────────
    def _start_tick(self):
        self.song_duration = 0.0
        self._timer = QTimer()
        self._timer.setInterval(500)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def _tick(self):
        if not self.state.is_playing or self.state.is_paused:
            return
        elapsed = self.state.current_position + (time.time() - self.state.last_update_time)
        if self.song_duration > 0:
            pct = min(int(elapsed / self.song_duration * 1000), 1000)
            self.seek_slider.setValue(pct)
            self.time_elapsed.setText(self._fmt(elapsed))

    @staticmethod
    def _fmt(secs):
        secs = max(0, int(secs))
        return f"{secs // 60}:{secs % 60:02d}"

    # ── playback actions (mirror original play_music logic) ───────────────────
    def _load_and_play(self, index):
        if not (0 <= index < len(self.music_files)):
            return
        self.current_index = index
        fname = self.music_files[index]
        path = os.path.join(self.SONGS_FOLDER, fname)
        pygame.mixer.music.load(path)

        self.state.current_position = 0.0
        self.state.last_update_time = time.time() # some arbitrary num
        self.state.is_paused = False
        self.state.is_playing = True

        pygame.mixer.music.play(start=self.state.current_position)

        # try to get duration via mutagen if available, else leave at 0
        try:
            from mutagen.mp3 import MP3
            self.song_duration = MP3(path).info.length
            self.time_total.setText(self._fmt(self.song_duration))
        except Exception:
            self.song_duration = 0.0
            self.time_total.setText("?:??")

        self.now_playing.setText(fname.strip(".mp3"))
        self.song_list.setCurrentRow(index)
        self.btn_play.setText("⏸")
        self.seek_slider.setValue(0)

    def _toggle_play(self):
        if not self.state.is_playing:
            # nothing loaded yet — play selected or first
            idx = self.song_list.currentRow()
            self._load_and_play(idx if idx >= 0 else 0)
            return
        if self.state.is_paused:
            pygame.mixer.music.unpause()
            self.state.is_paused = False
            self.state.last_update_time = time.time() # update again
            self.btn_play.setText("⏸")
        else:
            pygame.mixer.music.pause()
            self.state.current_position += time.time() - self.state.last_update_time #time.time is updated now and we subtract last updated time to get the difference
            # the difference indicates how much time has passed since the song has started
            self.state.is_paused = True
            self.btn_play.setText("▶")

    def _stop(self):
        pygame.mixer.music.stop()
        self.state.is_playing = False
        self.state.is_paused = False
        self.state.current_position = 0.0
        self.btn_play.setText("▶")
        self.seek_slider.setValue(0)
        self.time_elapsed.setText("0:00")

    def _rewind(self):
        # A: -5 seconds
        self.state.current_position = max(0, self.state.current_position - 5) # max() to avoid negative numbers
        pygame.mixer.music.play(start=self.state.current_position)
        self.state.last_update_time = time.time()

    def _forward(self):
        # D: +5 seconds
        self.state.current_position += 5
        pygame.mixer.music.play(start=self.state.current_position)
        self.state.last_update_time = time.time()

    def _prev_song(self):
        self._load_and_play(max(0, self.current_index - 1))

    def _next_song(self):
        self._load_and_play(min(len(self.music_files) - 1, self.current_index + 1))

    def _on_double_click(self, item):
        self._load_and_play(self.song_list.row(item))

    def _on_seek(self, value):
        if self.song_duration <= 0:
            return
        self.state.current_position = value / 1000 * self.song_duration
        pygame.mixer.music.play(start=self.state.current_position)
        self.state.last_update_time = time.time()
        self.time_elapsed.setText(self._fmt(self.state.current_position))
# ─────────────────────────────────────────────────────────────────────────────


def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print('error initializing!', e)
    folder = "songs"
    if not os.path.isdir(folder):
        print(f" folder '{folder}' not found!")
    music_files = [file for file in os.listdir(folder) if file.endswith('.mp3')] # checks if the files are mp3 then adds

    if not music_files:
        print('no mp3 files found!')
        return
    while True:
        print('Music app!')
        for i, songs in enumerate(music_files, start=1):
            print(f"{i}, {songs.strip('.mp3')}")
        choice = input("Choose the song by number, or press 'q' to quit: ")
        if choice.lower().strip() == "q":
            break
        elif not choice.isdigit():
            print("invalid input")
            continue
        else:
            music_choice_index = int(choice) - 1
            play_music(folder, music_files[music_choice_index])


if __name__ == "__main__":
    # ── launch GUI instead of the console main() ──────────────────────────────
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MusicPlayerWindow()
    window.show()
    sys.exit(app.exec())
    # ── the original main() is preserved above and can be restored anytime ────