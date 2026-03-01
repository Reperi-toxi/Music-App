import qrcode
from io import BytesIO

from app.network import get_local_ip
from app.player_handler import PlayerHandler
from app.music_player import MusicPlayer
from app.styles import (MAIN_LABEL_STYLE, TRACK_SLIDER_STYLE, BUTTON_STYLE,
                    VOLUME_SLIDER_STYLE, LIST_WIDGET_STYLE, CHECKBOX_STYLE)

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QSlider, QCheckBox, QDialog)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QTimer


class MainWindow(QMainWindow):
    width = 700  # size of main window
    height = 600

    def __init__(self):
        super().__init__()
        self.player = MusicPlayer("songs")
        self.setWindowTitle("Music App")
        self.setWindowIcon(QIcon("../Icon.png"))
        self.setGeometry(50, 50, self.width, self.height)
        self.setStyleSheet("Background-Color: rgb(8, 6, 59)")
        # Main blocks of app ---------------------------------------------------------
        self.timer: QTimer = QTimer()
        self.central_widget = QWidget()  # all bellow will be part of central
        self.title_widget = QWidget()
        self.track_container_widget = QWidget()
        self.buttons_widget = QWidget()
        self.extras_widget = QWidget()
        self.volume_container_widget = QWidget()
        self.music_list_widget: QListWidget = QListWidget()  # type hints to avoid warnings, annoying ah
        # Buttons labels and etc. ----------------------------------------------------
        self.play_button: QPushButton = QPushButton("Play", self.buttons_widget)
        self.stop_button: QPushButton = QPushButton("Stop", self.buttons_widget)
        self.forward_button: QPushButton = QPushButton("+5", self.buttons_widget)
        self.backward_button: QPushButton = QPushButton("-5", self.buttons_widget)

        self.auto_replay_checkbox: QCheckBox = QCheckBox("Auto-Replay ⟲", self.extras_widget)
        self.previous_button: QPushButton = QPushButton("<< Previous", self.extras_widget)
        self.next_button: QPushButton = QPushButton("Next >>", self.extras_widget)

        self.main_label = QLabel("Music Player", self.title_widget)

        self.track_slider: QSlider = QSlider()
        self.current_time_label = QLabel("0:00", self.track_container_widget)
        self.total_time_label = QLabel("0:00", self.track_container_widget)

        self.volume_slider: QSlider = QSlider()
        self.low_volume_label = QLabel("🔈", self.volume_container_widget)
        self.high_volume_label = QLabel("🔊", self.volume_container_widget)
        # layouts -----------------------------------------------------------------
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.track_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.extras_layout = QHBoxLayout()
        self.volume_layout = QHBoxLayout()

        # Assign to layouts ------------------------------------------------
        # add widgets to layouts

        self.main_layout.addWidget(self.title_widget, stretch=1)
        self.main_layout.addWidget(self.track_container_widget, stretch=2)
        self.main_layout.addWidget(self.buttons_widget, stretch=3)
        self.main_layout.addWidget(self.extras_widget, stretch=2)
        self.main_layout.addWidget(self.volume_container_widget, stretch=2)
        self.main_layout.addWidget(self.music_list_widget, stretch=8)

        self.title_layout.addWidget(self.main_label)

        self.track_layout.addWidget(self.current_time_label)
        self.track_layout.addWidget(self.track_slider)
        self.track_layout.addWidget(self.total_time_label)

        self.button_layout.addWidget(self.backward_button)
        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.forward_button)

        self.extras_layout.addWidget(self.previous_button)
        self.extras_layout.addWidget(self.auto_replay_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.extras_layout.addWidget(self.next_button)

        self.volume_layout.addWidget(self.low_volume_label)
        self.volume_layout.addWidget(self.volume_slider)
        self.volume_layout.addWidget(self.high_volume_label)
        # assigning layouts to main blocks
        self.central_widget.setLayout(self.main_layout)
        self.title_widget.setLayout(self.title_layout)
        self.track_container_widget.setLayout(self.track_layout)
        self.buttons_widget.setLayout(self.button_layout)
        self.extras_widget.setLayout(self.extras_layout)
        self.volume_container_widget.setLayout(self.volume_layout)

        self.music_list = self.player.music_files

        self.handle_song_labels()
        self.init_ui()
        self.show_qr()
        self.handler = PlayerHandler(self, self.player) # now this isntance handles all the logic
    def init_ui(self):
        # -- main label/title widget --------------------------------------------------------
        self.main_label.setFont(QFont("Consolas", 24))
        self.main_label.setStyleSheet(MAIN_LABEL_STYLE)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # -- Track ---------------------------------------------------------
        self.track_layout.setSpacing(20)
        self.current_time_label.setFont(QFont("", 20))
        self.total_time_label.setFont(QFont("", 20))

        self.track_slider.setOrientation(Qt.Orientation.Horizontal)
        self.track_slider.setRange(0, 100)  # arbitrary, updated later with timer
        self.track_slider.setValue(0)
        self.track_slider.setStyleSheet(TRACK_SLIDER_STYLE)
        # -- Buttons --------------------------------------------------------
        self.buttons_widget.setStyleSheet(BUTTON_STYLE)
        # .. Extras ---------------------------------------------------
        self.auto_replay_checkbox.setStyleSheet(CHECKBOX_STYLE)
        self.extras_widget.setStyleSheet(BUTTON_STYLE)
        # -- Volume -----------------------------------------------------------------------
        self.volume_layout.setSpacing(20)
        self.low_volume_label.setFont(QFont("", 20))
        self.high_volume_label.setFont(QFont("", 20))

        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 50)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet(VOLUME_SLIDER_STYLE)
        # -- List of songs widget ----------------------------------------------------------
        self.music_list_widget.setStyleSheet(LIST_WIDGET_STYLE)
        self.music_list_widget.setCurrentRow(0)

    def handle_song_labels(self):
        for song in self.music_list:
            self.music_list_widget.addItem(song.removesuffix(".mp3"))

    def show_qr(self):  # possibly temporary solution to connecting phone to the app
        ip = get_local_ip()
        url = f"http://{ip}:5000"

        img = qrcode.make(url)
        buf = BytesIO()
        img.save(buf, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        dialog = QDialog(self)
        dialog.setWindowTitle("Scan to connect")
        dialog.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        label = QLabel()
        label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        url_label = QLabel(url)
        url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        url_label.setStyleSheet("color: black; font-size: 12px;")
        layout.addWidget(label)
        layout.addWidget(url_label)
        dialog.setLayout(layout)
        dialog.show()
        self._qr_dialog = dialog