from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QWidget)
from music_player import MusicPlayer
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys


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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()

        self.play_button: QPushButton = QPushButton("Play", self)
        self.forward_button: QPushButton = QPushButton("+5", self)
        self.backward_button: QPushButton = QPushButton("-5", self)

        layout.addWidget(self.backward_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.forward_button)
        self.label = QLabel("Music App", self)
        central_widget.setLayout(layout)

        self.init_ui()
    def init_ui(self):
        # -- main label --------------------------------------------------------
        self.label.setFont(QFont("Consolas", 24))
        self.label.setGeometry(0, 0, self.width, 50)
        self.label.setStyleSheet("Color: rgb(4, 43, 94);"
                            "Background-Color: rgb(209, 232, 235)")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        # -- play button --------------------------------------------------------
        self.play_button.setGeometry(300, 200, 100, 100)
        self.play_button.setFont(QFont("Consolas", 16))
        self.play_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.play_button.clicked.connect(self.on_click_play)
        # -- forward button --------------------------------------------------------
        self.forward_button.setGeometry(300, 200, 100, 100)
        self.forward_button.setFont(QFont("Consolas", 16))
        self.forward_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.forward_button.clicked.connect(self.on_click_forward)
        # -- backward button --------------------------------------------------------
        self.backward_button.setGeometry(300, 200, 100, 100)
        self.backward_button.setFont(QFont("Consolas", 16))
        self.backward_button.setStyleSheet("Color: rgb(4, 43, 94);" 
                             "Background-Color: White;")
        self.backward_button.clicked.connect(self.on_click_backward)
    def on_click_play(self):
        self.player.load("Subhuman.mp3")
        self.player.play()
    def on_click_forward(self):
        self.player.go_forward()
    def on_click_backward(self):
        self.player.go_back()
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
