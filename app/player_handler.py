
from .network import RemoteSignals, start_remote, set_current_song
import random
from .music_player.states import MusicStates
# handling logic in this class, trying to leave UI only in MainWindow
class PlayerHandler:
    def __init__(self, window, player):
        self.window = window # :MainWindow temporarily, might have to change it if we use several windows

        self.player = player
        self.state_handler = self.player.state_handler

        self.play_from_beginning = True
        self.is_dragging = False

        self.window.track_slider.setDisabled(True)

        self.connect_signals()
        self.set_timer()
        self.setup_remote()

    def connect_signals(self):
        w = self.window

        w.backward_button.clicked.connect(self.on_click_backward)
        w.play_button.clicked.connect(self.on_click_play)
        w.stop_button.clicked.connect(self.on_click_stop)
        w.forward_button.clicked.connect(self.on_click_forward)
        w.previous_button.clicked.connect(self.on_click_previous)
        w.next_button.clicked.connect(self.on_click_next)

        w.music_list_widget.currentItemChanged.connect(self.on_click_song)

        w.track_slider.sliderPressed.connect(self.on_track_slider_pressed)
        w.track_slider.sliderReleased.connect(self.on_track_slider_released)

        w.volume_slider.valueChanged.connect(
            lambda value: self.on_change_volume(value / 50)
        )

        self.state_handler.state_changed.connect(self.on_state_changed)

    def set_timer(self):
        self.window.timer.setInterval(200)
        self.window.timer.timeout.connect(self.check_song_end)
        self.window.timer.timeout.connect(self.update_time_label)
        self.window.timer.timeout.connect(self.update_track_slider)
        self.window.timer.start()

    def update_time_label(self):
        pos_seconds = self.player.get_position() or 0.0
        minutes = int(pos_seconds // 60)
        seconds = int(pos_seconds % 60)
        self.window.current_time_label.setText(f"{minutes}:{seconds:02}")


    def on_state_changed(self, state):
        w = self.window
        if state == MusicStates.STOPPED:
            w.play_button.setText("Play")
            w.main_label.setText("Music Player")
            w.total_time_label.setText("0:00")
            w.track_slider.setDisabled(True)
        if state == MusicStates.PLAYING:
            w.play_button.setText("Pause")
            w.track_slider.setEnabled(True)
        if state == MusicStates.PAUSED:
            w.play_button.setText("Resume")
            w.track_slider.setEnabled(True)

    def load_and_play(self, song_name):
        self.player.load(song_name + ".mp3")
        self.player.play()

        length = self.player.get_song_length(song_name + ".mp3") or 0.0
        minutes = int(length // 60)
        seconds = int(length % 60)

        self.window.total_time_label.setText(f"{minutes}:{seconds:02}")
        self.window.track_slider.setMaximum(int(length))
        self.window.main_label.setText(song_name)
        set_current_song(song_name)
        self.play_from_beginning = False
        self.window.music_list_widget.mark_playing(self.window.music_list_widget.currentRow())

    def on_click_play(self):
        w = self.window
        if self.play_from_beginning:
            current_song = w.music_list_widget.currentItem()
            if current_song is None:
                return
            self.load_and_play(current_song.text())
        else:
            if self.state_handler.is_state(MusicStates.PAUSED):
                self.player.resume()
            elif self.state_handler.is_state(MusicStates.PLAYING):
                self.player.pause()

    def on_click_stop(self):
        w = self.window
        self.player.stop()
        self.play_from_beginning = True

    def on_click_song(self):
        w = self.window
        self.player.stop()
        current_song = w.music_list_widget.currentItem()
        if current_song is None:
            return
        self.load_and_play(current_song.text())

    def on_click_next(self):
        w = self.window
        current_index = w.music_list_widget.currentRow()
        next_index = current_index + 1
        if next_index < w.music_list_widget.count():
            w.music_list_widget.setCurrentRow(next_index)
            self.load_and_play(w.music_list_widget.currentItem().text())

    def on_click_previous(self):
        w = self.window
        current_index = w.music_list_widget.currentRow()
        previous_index = current_index - 1
        if current_index > 0:
            w.music_list_widget.setCurrentRow(previous_index)
            self.load_and_play(w.music_list_widget.currentItem().text())

    def on_click_forward(self):
        self.player.go_forward()

    def on_click_backward(self):
        self.player.go_back()

    def on_change_volume(self, volume):
        self.player.set_volume(volume)
    def on_track_slider_pressed(self):
        self.is_dragging = True
        self.player.pause()

    def on_track_slider_released(self):
        self.is_dragging = False
        self.on_change_track()

    def on_change_track(self):
        if not self.is_dragging:
            self.player.play(position=self.window.track_slider.value())

    def update_track_slider(self):
        if not self.is_dragging:
            self.window.track_slider.blockSignals(True)
            self.window.track_slider.setValue(int(self.player.get_position()))
            self.window.track_slider.blockSignals(False)

    def check_song_end(self):
        w = self.window
        current_song = w.music_list_widget.currentItem()
        if self.state_handler.state == MusicStates.PLAYING and not self.player.get_busy():
            if w.auto_replay_checkbox.isChecked():  # auto replaying
                if current_song:
                    self.load_and_play(current_song.text())
            elif w.shuffle_checkbox.isChecked():   # shuffling
                random_row = random.randrange(w.music_list_widget.count())
                if current_song:
                    w.music_list_widget.setCurrentRow(random_row)

            else:  # none selected, move to next
                w.music_list_widget.setCurrentRow(w.music_list_widget.currentRow() + 1)
                current_song = w.music_list_widget.currentItem()
                self.load_and_play(current_song.text())


    def setup_remote(self):
        self._sig = RemoteSignals()
        self._sig.play.connect(self.on_click_play)
        self._sig.stop.connect(self.on_click_stop)
        self._sig.previous.connect(self.on_click_previous)
        self._sig.next.connect(self.on_click_next)
        self._sig.backward.connect(self.on_click_backward)
        self._sig.forward.connect(self.on_click_forward)
        start_remote(self._sig)