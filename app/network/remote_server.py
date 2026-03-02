import socket
import json
import os
import threading
from flask import Flask
from PyQt6.QtCore import QObject, pyqtSignal

current_song = {"name": "Music Player"}

def HTML():
    file_path = os.path.join(os.path.dirname(__file__), "remote.html")

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    return html.replace("{{song_name}}", current_song["name"])


class RemoteSignals(QObject):
    play = pyqtSignal()
    stop = pyqtSignal()
    previous = pyqtSignal()
    next = pyqtSignal()
    backward = pyqtSignal()
    forward = pyqtSignal()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def set_current_song(name: str):
    current_song["name"] = name if name else "Music Player"


def start_remote(signals, port=5000):
    app = Flask(__name__)

    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    @app.route("/song")
    def song():
        return app.response_class(
            response=json.dumps({"name": current_song["name"]}),
            mimetype="application/json"
        )
    @app.route("/play")
    def play():     signals.play.emit();     return HTML()
    @app.route("/stop")
    def stop():     signals.stop.emit();     return HTML()
    @app.route("/prev")
    def prev():     signals.previous.emit(); return HTML()
    @app.route("/next")
    def next():     signals.next.emit();     return HTML()
    @app.route("/back")
    def back():     signals.backward.emit(); return HTML()
    @app.route("/fwd")
    def fwd():      signals.forward.emit();  return HTML()
    @app.route("/")
    def index():    return HTML()

    print(f"Remote: http://{get_local_ip()}:{port}")
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port, use_reloader=False), daemon=True).start()