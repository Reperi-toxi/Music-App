from enum import Enum, auto
from PyQt6.QtCore import pyqtSignal, QObject

class MusicStates(Enum):
    LOADED = auto() # just in case
    PLAYING = auto()
    STOPPED = auto()
    PAUSED = auto()

class StateHandler(QObject):
    state_changed: pyqtSignal = pyqtSignal(MusicStates)
    def __init__(self):
        super().__init__()
        self.state = MusicStates.STOPPED
    def change_state(self, state):
        self.state = state
        self.state_changed.emit(state)

    def is_state(self, state):
        return self.state == state