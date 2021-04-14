import itertools
import json
import logging
import select
import os

seen_macs = []


def read_fifo_until_closed(fifo_name):
    global seen_macs
    if os.path.isfile('bt.txt'):
        logging.debug('loading MACs from bt.txt')
        with open('bt.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                loaded = json.loads(line)
                mac_addr = loaded['MAC']
                logging.info('Loaded pre-existing MAC: [%s]', mac_addr)
                seen_macs.append(mac_addr)
        logging.debug('finished loading MACs')
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
            with open('bt.txt', 'a') as f:
                f.write(json.dumps(loaded))
                f.write('\n')
        logging.error('stopped reading fifo!')
