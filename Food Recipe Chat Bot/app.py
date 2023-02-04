from flask import Flask, render_template
from flask_socketio import SocketIO

from backend.interaction_manager import InteractionManager
from backend.socketmanager import SocManager

app = Flask(__name__)
app.static_folder = 'static'

socketio = SocketIO(app)
socManager = SocManager()
socManager.set_socket(socketio)

@app.route("/")
def hello_world():
    return render_template("index.html")

@socketio.on("start")
def start():
    global socManager

    im = InteractionManager(socManager)
    im.startInteraction()

if __name__ == "__main__":
    socketio.run(app, debug=True)