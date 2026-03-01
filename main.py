import sys
from app.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()