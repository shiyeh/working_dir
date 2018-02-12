#!/usr/bin/python

import os
import sys
import collections
import socket
import json
import copy
import logging

log = logging.getLogger(__name__)
LOG_PATH = '/tmp/db_sender.log'


def db_sock_send(query):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect("/tmp/db.sock")
        s.send(query)
        data = s.recv(10240)
        data = json.loads(data)
    except Exception as e:
        log.info(str(e))
    return data


def db_reset():
    log.info('db_reset start')
    os.system('cp /opt/mlis/conf/app.db.bak /tmp/app.db')
    os.system('cp /opt/mlis/conf/app.db.bak /opt/mlis/web_console/app/app.db')
    os.system('cp /opt/mlis/conf/status.db.bak /opt/mlis/web_console/app/status.db')
    # update DATABASE in daemon
    db_sock_send('{"method": "update"}')
    log.info('db_reset end')


def db_export(path='/tmp/g420x.json'):
    log.info('db_export start')
    data = db_sock_send('{"method": "dump"}')
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=2)
    log.info('db_export end')


def db_import(path='/tmp/g420x.json'):
    log.info('db_import start')
    querys = []
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        for table, records in data.items():
            if type(records) is not list:
                continue
            query = {'method': 'set'}
            query['table'] = table
            query['values'] = {}
            for record in records:
                if table == 'user' and record.get("id") < 3:
                    continue
                for key, value in record.items():
                    if key == 'id':
                        query['id'] = value
                    else:
                        query['values'][key] = \
                            value if str(value) != 'None' else None
                querys.append(copy.deepcopy(query))
    except Exception as e:
        return str(e)

    # reset db, to remove old data in db
    db_reset()
    
    log.info('**********start import***********')
    for query in querys:
        rslt = db_sock_send(json.dumps(query))
        if 'success' not in json.dumps(rslt):
            log.info('**********data error*************')
            log.info(json.dumps(query))
            log.info(json.dumps(rslt))
    log.info('**********end import*************')
    log.info('db_import end')


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
                        format='%(asctime)s %(levelname)s: %(message)s')
    _funcs = {'reset': db_reset,
              'export': db_export,
              'import': db_import,}
    if len(sys.argv) == 1:
        print 'check format'
    if len(sys.argv) == 2:
        _funcs[sys.argv[1]]()
    if len(sys.argv) == 3:
        _funcs[sys.argv[1]](sys.argv[2])
