import os

from flask import Flask
from flask_socketio import SocketIO, emit

FRONTEND_ORIGIN = "http://127.0.0.1:3000"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=[FRONTEND_ORIGIN])

@app.route('/')
def index():
    return "Connect with Socket.IO!"

@socketio.on('connect')
def test_connect():
    emit('NewData', {'data':'hello, world'})

if __name__ == '__main__':
    socketio.run(app)
