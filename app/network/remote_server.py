import socket
import json
import threading
from flask import Flask
from PyQt6.QtCore import QObject, pyqtSignal

current_song = {"name": "Music Player"}

def HTML():
    return f"""<!DOCTYPE html>
                <html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                  body {{ background:#111; display:flex; flex-wrap:wrap; gap:12px; padding:20px; justify-content:center; }}
                  h1   {{ width:100%; text-align:center; color:#fff; font-family:sans-serif;
                          font-size:1rem; font-weight:normal; margin:0 0 8px; }}
                  a    {{ display:flex; align-items:center; justify-content:center;
                         width:120px; height:80px; background:#222; color:#fff;
                         font-size:1.1rem; font-family:sans-serif; text-decoration:none;
                         border-radius:12px; border:1px solid #444; }}
                  a:active {{ background:#444; }}
                </style>
                </head>
                <body>
                  <h1 id="title">{current_song["name"]}</h1>
                  <a onclick="cmd('/play')">▶ / ⏸</a>
                  <a onclick="cmd('/stop')">⏹ Stop</a>
                  <a onclick="cmd('/prev')">⏮ Prev</a>
                  <a onclick="cmd('/next')">⏭ Next</a>
                  <a onclick="cmd('/back')">-5s</a>
                  <a onclick="cmd('/fwd')">+5s</a>
                <script>
                  async function cmd(action) {{
                    await fetch(action);
                    setTimeout(async () => {{
                      const r = await fetch('/song');
                      const d = await r.json();
                      document.getElementById('title').textContent = d.name;
                    }}, 300);
                  }}
                </script>
                </body>
                </html>"""


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