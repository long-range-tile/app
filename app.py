import os

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'Hello, world'

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

if __name__ == '__main__':
    socketio.run(app)
