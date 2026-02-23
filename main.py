import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QSlider)
from music_player import MusicPlayer
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    width = 700  # size of main window
    height = 600

    def __init__(self):
        super().__init__()
        self.player = MusicPlayer("songs")
        self.setWindowTitle("Music App")
        self.setWindowIcon(QIcon("Icon.png"))
        self.setGeometry(50, 50, self.width, self.height)
        self.setStyleSheet("Background-Color: rgb(8, 6, 59)")
        # Main blocks of app ---------------------------------------------------------
        self.timer: QTimer = QTimer()
        self.central_widget = QWidget()  # all bellow will be part of central
        self.title_widget = QWidget()
        self.track_container_widget = QWidget()
        self.buttons_widget = QWidget()
        self.volume_container_widget = QWidget()
        self.music_list_widget: QListWidget = QListWidget()  # type hints to avoid warnings, annoying ah
        # Buttons labels and etc. ----------------------------------------------------
        self.play_button: QPushButton = QPushButton("Play", self.buttons_widget)
        self.stop_button: QPushButton = QPushButton("Stop", self.buttons_widget)
        self.forward_button: QPushButton = QPushButton("+5", self.buttons_widget)
        self.backward_button: QPushButton = QPushButton("-5", self.buttons_widget)

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
        self.volume_layout = QHBoxLayout()
        self.music_list_layout = QVBoxLayout()
        # Assign to layouts ------------------------------------------------
        # add widgets to layouts
        self.main_layout.addWidget(self.title_widget, stretch=1)
        self.main_layout.addWidget(self.track_container_widget, stretch=2)
        self.main_layout.addWidget(self.buttons_widget, stretch=3)
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

        self.volume_layout.addWidget(self.low_volume_label)
        self.volume_layout.addWidget(self.volume_slider)
        self.volume_layout.addWidget(self.high_volume_label)
        # assigning layouts to main blocks
        self.central_widget.setLayout(self.main_layout)
        self.title_widget.setLayout(self.title_layout)
        self.track_container_widget.setLayout(self.track_layout)
        self.buttons_widget.setLayout(self.button_layout)
        self.volume_container_widget.setLayout(self.volume_layout)
        self.music_list_widget.setLayout(self.music_list_layout)

        self.music_list = self.player.music_files
        self.play_from_beginning = True
        self.is_dragging = False
        self.handle_song_labels()

        self.init_ui()
        self.set_timer()

    def init_ui(self):
        # -- main label/title widget --------------------------------------------------------
        self.main_label.setFont(QFont("Consolas", 24))
        self.main_label.setStyleSheet("Color: rgb(4, 43, 94);"
                                      "Background-Color: rgb(209, 232, 235);"
                                      "Border-radius: 5px")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # -- Track ---------------------------------------------------------
        self.track_layout.setSpacing(20)
        self.current_time_label.setFont(QFont("", 20))
        self.total_time_label.setFont(QFont("", 20))

        self.track_slider.setOrientation(Qt.Orientation.Horizontal)
        self.track_slider.setRange(0, 100)  # arbitrary, updated later with timer
        self.track_slider.setValue(0)
        self.track_slider.setStyleSheet("""
                    QSlider::groove:horizontal {
                        height: 6px;
                        background: rgb(26, 25, 107);
                        border-radius: 3px;
                        border: 1px solid white;
                    }
                    QSlider::handle:horizontal {
                        background: white;
                        width: 16px;
                        height: 16px;
                        margin: -5px 0;
                        border-radius: 8px;
                    }
                    QSlider::sub-page:horizontal {
                        background: rgb(209, 232, 235);
                        border-radius: 3px;
                    }
                """)

        self.track_slider.sliderPressed.connect(self.on_track_slider_pressed)
        self.track_slider.sliderReleased.connect(self.on_track_slider_released)
        # -- Buttons --------------------------------------------------------
        self.buttons_widget.setStyleSheet("""
            QPushButton {
                font-family: consolas;
                font-size: 16pt;
                color: rgb(4, 43, 94);
                background-color: white;
            }
            QPushButton:hover {
                background-color: rgb(230, 230, 230);
            }
            QPushButton:pressed {
                background-color: rgb(4, 43, 94);
                color: white;
            }
        """)
        # -- Button functionalities ------------------------------------------------------
        self.backward_button.clicked.connect(self.on_click_backward)
        self.play_button.clicked.connect(self.on_click_play)
        self.stop_button.clicked.connect(self.on_click_stop)
        self.forward_button.clicked.connect(self.on_click_forward)
        # -- Volume -----------------------------------------------------------------------
        self.volume_layout.setSpacing(20)
        self.low_volume_label.setFont(QFont("", 20))
        self.high_volume_label.setFont(QFont("", 20))

        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 50)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgb(26, 25, 107);
                border-radius: 3px;
                border: 1px solid white;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: rgb(209, 232, 235);
                border-radius: 3px;
            }
        """)
        self.volume_slider.valueChanged.connect(lambda value: self.on_change_volume(value / 50))
        # -- List of songs widget ----------------------------------------------------------
        self.music_list_widget.setStyleSheet("""
            QListWidget {
                background-color: rgb(26, 25, 107);
                color: White;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget:focus {
                outline: none;
            }
            QListWidget::item:hover {
                Color: rgb(4, 43, 94);
                background-color: #b8b8e3;
            }
            QListWidget::item:selected:hover {
                Color: White;
                background-color: #2c2cf5;
            }
            QScrollBar:vertical {
                background: rgb(26, 25, 107);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgb(209, 232, 235);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: white;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        # self.music_list_widget.clicked.connect(self.on_click_song)

    def set_timer(self):
        self.timer.setInterval(200)  # checks every 0.2 seconds
        self.timer.timeout.connect(self.check_song_end)  # check whether song has ended
        self.timer.timeout.connect(self.update_time_label)  # update current time label
        self.timer.timeout.connect(self.update_track_slider)
        self.timer.start()

    def update_time_label(self):
        pos_seconds = self.player.get_position() or 0.0
        minutes = int(pos_seconds // 60)
        seconds = int(pos_seconds % 60)
        time_str = f"{minutes}:{seconds:02}"  # formatting to minutes:seconds, :02 to maek it two digit
        self.current_time_label.setText(time_str)

    # -- handling track slider -----------------------------------
    def on_track_slider_pressed(self):
        self.is_dragging = True
        self.player.pause()

    def on_track_slider_released(self):
        self.is_dragging = False
        self.on_change_track()

    def update_track_slider(self):
        if not self.is_dragging:
            self.track_slider.blockSignals(True)
            self.track_slider.setValue(int(self.player.get_position()))
            self.track_slider.blockSignals(False)
    # -------------------------------------------------------------
    def check_song_end(self):
        if not self.player.get_busy() and self.player.is_playing and not self.player.is_paused:
            # song ended naturally
            self.player.pause()
            self.play_from_beginning = True
            self.play_button.setText("Play")

    def on_click_play(self):
        if self.play_from_beginning:
            current_song = self.music_list_widget.currentItem()
            if current_song is None:
                return
            self.main_label.setText(current_song.text().removesuffix(".mp3"))
            self.player.load(current_song.text() + ".mp3")
            self.player.play()

            pos_seconds = self.player.get_song_length(current_song.text() + ".mp3") or 0.0
            minutes = int(pos_seconds // 60)
            seconds = int(pos_seconds % 60)
            time_str = f"{minutes}:{seconds:02}"

            self.play_button.setText("Pause")
            self.total_time_label.setText(time_str)
            self.track_slider.setMaximum(int(self.player.get_song_length(current_song.text() + ".mp3")))
            self.play_from_beginning = False
        else:
            if self.player.is_paused:
                self.player.resume()
                self.play_button.setText("Pause")
            else:
                self.player.pause()
                self.play_button.setText("Resume")

    def on_click_stop(self):
        self.player.stop()
        self.play_from_beginning = True
        self.play_button.setText("Play")
        self.main_label.setText("Music Player")
        self.total_time_label.setText("0:00")

    def on_click_forward(self):
        if self.player.is_paused:
            self.play_button.setText("Pause")
        self.player.go_forward()

    def on_click_backward(self):
        if self.player.is_paused:
            self.play_button.setText("Pause")
        self.player.go_back()

    def on_click_song(self):
        self.player.stop()
        self.play_from_beginning = True
        self.play_button.setText("Play")

    def on_change_volume(self, volume):
        self.player.set_volume(volume)

    def on_change_track(self):
        if self.player.is_playing and not self.is_dragging:
            self.player.play(position=self.track_slider.value())
            self.play_button.setText("Pause")
    def handle_song_labels(self):
        for song in self.music_list:
            self.music_list_widget.addItem(song.removesuffix(".mp3"))

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()