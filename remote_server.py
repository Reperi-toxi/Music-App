import socket
import threading
from flask import Flask
from PyQt6.QtCore import QObject, pyqtSignal

HTML = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { background:#111; display:flex; flex-wrap:wrap; gap:12px; padding:20px; justify-content:center; }
  a    { display:flex; align-items:center; justify-content:center;
         width:120px; height:80px; background:#222; color:#fff;
         font-size:1.1rem; font-family:sans-serif; text-decoration:none;
         border-radius:12px; border:1px solid #444; }
  a:active { background:#444; }
</style>
</head>
<body>
  <a href="/play">▶ / ⏸</a>
  <a href="/stop">⏹ Stop</a>
  <a href="/prev">⏮ Prev</a>
  <a href="/next">⏭ Next</a>
  <a href="/back">-5s</a>
  <a href="/fwd">+5s</a>
</body>
</html>"""


class RemoteSignals(QObject):
    play     = pyqtSignal()
    stop     = pyqtSignal()
    previous = pyqtSignal()
    next     = pyqtSignal()
    backward = pyqtSignal()
    forward  = pyqtSignal()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def start_remote(signals, port=5000):
    app = Flask(__name__)

    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    @app.route("/play")
    def play():     signals.play.emit();     return HTML
    @app.route("/stop")
    def stop():     signals.stop.emit();     return HTML
    @app.route("/prev")
    def prev():     signals.previous.emit(); return HTML
    @app.route("/next")
    def next():     signals.next.emit();     return HTML
    @app.route("/back")
    def back():     signals.backward.emit(); return HTML
    @app.route("/fwd")
    def fwd():      signals.forward.emit();  return HTML
    @app.route("/")
    def index():    return HTML

    print(f"Remote: http://{get_local_ip()}:{port}")
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port, use_reloader=False), daemon=True).start()