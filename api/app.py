import os
import sys
import threading
import json
import logging
from signal import signal, SIGINT
import time
from pathlib import Path

import pi

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='./static/static',
            template_folder='./static')
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    pass


@socketio.on('gps_data')
def gps_data(data):
    data_dir = Path(os.getenv('DATA_DIR') or "./")
    gps_f = str((data_dir / 'gps.txt').resolve())
    with open(gps_f, 'a') as f:
        f.write(json.dumps(data))
        f.write('\n')
    socketio.emit('got_gps', time.time()*1000)


def sigint_handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully.')
    os._exit(1)


if __name__ == '__main__':
    signal(SIGINT, sigint_handler)
    logging.basicConfig(level=logging.DEBUG)
    port = 5000
    fifo_thread = threading.Thread(
        target=pi.read_fifo_until_closed, args=['/tmp/fifo1'])
    fifo_thread.start()
    logging.info('Server started on port %d.', port)
    socketio.run(app, host='0.0.0.0', port=port)
