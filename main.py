import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget)
from music_player import MusicPlayer
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt



class MainWindow(QMainWindow):
    width = 700 # size of main window
    height = 500
    player = MusicPlayer("songs")
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music App")
        self.setWindowIcon(QIcon("Icon.png"))
        self.setGeometry(50, 50, self.width, self.height)
        self.setStyleSheet("Background-Color: rgb(8, 6, 59)")
        # Main blocks of app ---------------------------------------------------------
        self.central_widget = QWidget() # all 3 bellow will be part of central
        self.title_widget = QWidget()
        self.buttons_widget = QWidget()
        self.music_list_widget = QWidget()

        # Buttons labels and etc. ----------------------------------------------------
        self.play_button : QPushButton = QPushButton("Play", self.buttons_widget)
        self.stop_button: QPushButton = QPushButton("Stop", self.buttons_widget)
        self.forward_button : QPushButton = QPushButton("+5", self.buttons_widget)
        self.backward_button : QPushButton = QPushButton("-5", self.buttons_widget)
        self.main_label = QLabel("Music App", self.title_widget)
        # layouts -----------------------------------------------------------------
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.music_list_layout = QVBoxLayout()
        # Assign to layouts -----------------------------------------
        # add widgets to layouts
        self.main_layout.addWidget(self.title_widget, stretch=1)
        self.main_layout.addWidget(self.buttons_widget, stretch=3)
        self.main_layout.addWidget(self.music_list_widget, stretch=8)

        self.title_layout.addWidget(self.main_label)

        self.button_layout.addWidget(self.backward_button)
        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.forward_button)
        # assigning layouts to main blocks
        self.central_widget.setLayout(self.main_layout)
        self.title_widget.setLayout(self.title_layout)
        self.buttons_widget.setLayout(self.button_layout)
        self.music_list_widget.setLayout(self.music_list_layout)

        self.init_ui()

        self.song_widgets = []
        self.play_from_beginning = True

    def init_ui(self):
        # -- main label/title widget --------------------------------------------------------

        self.main_label.setFont(QFont("Consolas", 24))
        self.main_label.setStyleSheet("Color: rgb(4, 43, 94);"
                            "Background-Color: rgb(209, 232, 235)")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # -- play button --------------------------------------------------------
        self.play_button.setGeometry(300, 200, 100, 100)
        self.play_button.setFont(QFont("Consolas", 16))
        self.play_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.play_button.clicked.connect(self.on_click_play)
        # -- Stop button --------------------------------------------------------
        self.stop_button.setGeometry(300, 200, 100, 100)
        self.stop_button.setFont(QFont("Consolas", 16))
        self.stop_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.stop_button.clicked.connect(self.on_click_stop)
        # -- forward button --------------------------------------------------------
        self.forward_button.setFont(QFont("Consolas", 16))
        self.forward_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.forward_button.clicked.connect(self.on_click_forward)
        # -- backward button --------------------------------------------------------
        self.backward_button.setFont(QFont("Consolas", 16))
        self.backward_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.backward_button.clicked.connect(self.on_click_backward)
        # -- Lists of songs widget ----------------------------------------------------------
        self.music_list_widget.setStyleSheet("Background-color: Red;"
                                             "Border: 3px solid white;"
                                             "Border-Radius: 5px")

    def on_click_play(self):
        if self.play_from_beginning:
            self.player.load("Subhuman.mp3")
            self.player.play()
            self.play_button.setText("Pause")
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
    def on_click_forward(self):
        self.player.go_forward()
    def on_click_backward(self):
        self.player.go_back()
    def handle_song_labels(self):
        pass
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
