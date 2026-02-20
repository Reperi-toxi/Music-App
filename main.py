from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel)
from music_player.player import MusicPlayer
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    width = 700 # size of main window
    height = 500
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music App")
        self.setWindowIcon(QIcon("Icon.png"))
        self.setGeometry(50, 50, self.width, self.height)
        self.setStyleSheet("Background-Color: rgb(8, 6, 59)")

        self.init_ui()
    def init_ui(self):
        label = QLabel("Music App", self)
        label.setFont(QFont("Consolas", 24))
        label.setGeometry(0, 0, self.width, 50)
        label.setStyleSheet("Color: rgb(4, 43, 94);"
                            "Background-Color: rgb(209, 232, 235)")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

def main():
    app = QApplication([])
    player = MusicPlayer()
    window = MainWindow(player)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
