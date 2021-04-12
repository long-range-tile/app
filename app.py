import os
import eventlet

import pi

from flask import Flask
from flask_socketio import SocketIO, emit

FRONTEND_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]
UPDATE_INTERVAL_SEC = 0.08

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=FRONTEND_ORIGINS)

@app.route('/')
def index():
    return "Connect with Socket.IO!"

@socketio.on('connect')
def emit_current_data():
    socketio.emit('NewData', pi.get_data())

@socketio.on('gps_data')
def gps_data(data):
    print('gps', data)
    pass

def run_timer():
    while True:
        eventlet.spawn(emit_current_data).wait()
        eventlet.sleep(UPDATE_INTERVAL_SEC)

if __name__ == '__main__':
    port = 5000
    eventlet.spawn(run_timer)
    t = eventlet.spawn(socketio.run, app, port=port)
    print(f'Server started on port {port}.')
    t.wait()
