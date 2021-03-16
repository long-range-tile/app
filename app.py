import os
import eventlet

from flask import Flask
from flask_socketio import SocketIO, emit

FRONTEND_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]
UPDATE_INTERVAL_SEC = 1

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=FRONTEND_ORIGINS)

test_counter = 1

@app.route('/')
def index():
    return "Connect with Socket.IO!"

@socketio.on('connect')
def emit_current_data():
    global test_counter
    socketio.emit('NewData', {'data':'hello, world', 'counter': test_counter})
    test_counter += 1

def run_timer():
    while True:
        eventlet.spawn(emit_current_data).wait()
        eventlet.sleep(UPDATE_INTERVAL_SEC)

if __name__ == '__main__':
    eventlet.spawn(run_timer)
    eventlet.spawn(socketio.run, app).wait()
