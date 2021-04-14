import itertools
import json
import logging
import select
import os
from pathlib import Path

seen_macs = []


def read_fifo_until_closed(fifo_name):
    global seen_macs
    data_dir = Path(os.getenv('DATA_DIR') or "./")
    bt_path = data_dir / 'bt.txt'
    bt_f = str(bt_path.resolve())
    bt_path.touch()
    logging.debug('loading MACs from bt.txt')
    with open(bt_f, 'r') as f:
        lines = f.readlines()
        for line in lines:
            loaded = json.loads(line)
            mac_addr = loaded['MAC']
            logging.info('Loaded pre-existing MAC: [%s]', mac_addr)
            seen_macs.append(mac_addr)
    logging.debug('finished loading MACs')
    while True:
        with open(fifo_name) as fifo:
            while True:
                select.select([fifo], [], [fifo])
                logging.debug('fifo data available!')
                data = fifo.readline()
                logging.debug('data read')
                if len(data) <= 0:
                    logging.error('Bad data length: [%d]', len(data))
                    break
                logging.debug(data)
                try:
                    loaded = json.loads(data)
                except json.decoder.JSONDecodeError as e:
                    logging.error('Error decoding JSON: %s', e)
                    continue
                if 'MAC' not in loaded:
                    logging.error('Saw packet with no MAC!')
                    continue
                mac_addr = loaded['MAC']
                if mac_addr in seen_macs:
                    continue
                logging.info('new MAC logged: [%s]', mac_addr)
                seen_macs.append(mac_addr)
                with open(bt_f, 'a') as f:
                    f.write(json.dumps(loaded))
                    f.write('\n')
            logging.error('stopped reading fifo!')
