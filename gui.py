from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt6.QtGui import QIcon, QFont
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music App")
        self.setWindowIcon(QIcon("Icon.png"))
        self.setGeometry(50, 50, 700, 500)

        label = QLabel("Music App", self)
        label.setFont(QFont("Consolas", 24))
        label.setGeometry(0, 0, 200, 100)
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

main()


    
