from network import RemoteSignals, start_remote, set_current_song

# handling logic in this class, trying to leave UI only in MainWindow
class PlayerHandler:
    def __init__(self, window, player):
        self.window = window
        self.player = player

        self.play_from_beginning = True
        self.is_dragging = False

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

        w.music_list_widget.clicked.connect(self.on_click_song)

        w.track_slider.sliderPressed.connect(self.on_track_slider_pressed)
        w.track_slider.sliderReleased.connect(self.on_track_slider_released)

        w.volume_slider.valueChanged.connect(
            lambda value: self.on_change_volume(value / 50)
        )

    def setup_remote(self):
        self._sig = RemoteSignals()
        self._sig.play.connect(self.on_click_play)
        self._sig.stop.connect(self.on_click_stop)
        self._sig.previous.connect(self.on_click_previous)
        self._sig.next.connect(self.on_click_next)
        self._sig.backward.connect(self.on_click_backward)
        self._sig.forward.connect(self.on_click_forward)
        start_remote(self._sig)

    # ---- ALL YOUR ORIGINAL METHODS BELOW (UNCHANGED LOGIC) ----
    # (Just replace self -> self.window where accessing UI)

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
        self.window.play_button.setText("Pause")
        self.play_from_beginning = False

    def on_click_play(self):
        w = self.window
        if self.play_from_beginning:
            current_song = w.music_list_widget.currentItem()
            if current_song is None:
                return
            self.load_and_play(current_song.text())
        else:
            if self.player.is_paused:
                self.player.resume()
                w.play_button.setText("Pause")
            else:
                self.player.pause()
                w.play_button.setText("Resume")

    def on_click_stop(self):
        w = self.window
        self.player.stop()
        self.play_from_beginning = True
        w.play_button.setText("Play")
        w.main_label.setText("Music Player")
        w.total_time_label.setText("0:00")

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
        if self.player.is_paused:
            self.window.play_button.setText("Pause")
        self.player.go_forward()

    def on_click_backward(self):
        if self.player.is_paused:
            self.window.play_button.setText("Pause")
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
        if self.player.is_playing and not self.is_dragging:
            self.player.play(position=self.window.track_slider.value())
            self.window.play_button.setText("Pause")

    def update_track_slider(self):
        if not self.is_dragging:
            self.window.track_slider.blockSignals(True)
            self.window.track_slider.setValue(int(self.player.get_position()))
            self.window.track_slider.blockSignals(False)

    def check_song_end(self):
        w = self.window
        if not self.player.get_busy() and self.player.is_playing and not self.player.is_paused:
            if w.auto_replay_checkbox.isChecked():
                current_song = w.music_list_widget.currentItem()
                if current_song:
                    self.player.load(current_song.text() + ".mp3")
                    self.player.play()
            else:
                self.player.pause()
                self.play_from_beginning = True
                w.play_button.setText("Play")