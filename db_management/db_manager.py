#!/usr/bin/env python

import sys
import time
import os
import socket
import sqlite3
import json

import threading
from daemon import Daemon
from db_confirm import db_confirm

db_sock = "/tmp/db.sock"
DBs = ["/tmp/cellular.db",
       "/tmp/app.db",
       "/tmp/status.db"]
pidfile = "/tmp/db_manager.pid"
### The global LOCK for make sure only one thread using database at same time.
LOCK = threading.RLock()


class dbUpdate(threading.Thread):
    def __init__(self):
        super(dbUpdate, self).__init__()
        self.dbs = DBs

    def run(self):
        global DATABASE, DB_CHANGED
        DB_CHANGED = False
        LOCK.acquire()
        DATABASE = {}
        for idx, db in enumerate(self.dbs):
            while not os.path.exists(db):
                time.sleep(1)
            sqldb = sqlite(db)
            DATABASE.update(sqldb.dumpData())

        sqldb = sqlite("/tmp/status.db")
        ts = {
            "method": "set",
            "table": "system_info",
            "id": 1,
            "values": {"up_time": time.time()}
        }
        sqldb.setData(ts)

        LOCK.release()
        while True:
            if DB_CHANGED:
                LOCK.acquire()
                DATABASE = {}
                for idx, db in enumerate(self.dbs):
                    if os.path.exists(db):
                        sqldb = sqlite(db)
                        DATABASE.update(sqldb.dumpData())
                LOCK.release()
            else:
                if os.path.exists(self.dbs[0]):
                    sqldb = sqlite(self.dbs[0])
                    DATABASE.update(sqldb.dumpData())

            time.sleep(10)


class sqlite(object):
    def __init__(self, sqlite):
        self.sqlite = sqlite

    def dict_factory(self, cursor, row):
        d = {}
        for index, column in enumerate(cursor.description):
            d[column[0]] = row[index]
        return d

    def getData(self, table):
        connection = sqlite3.connect(self.sqlite)
        connection.row_factory = self.dict_factory
        cursor = connection.cursor()
        cursor.execute("select * from " + table)
        # fetch all or one we'll go for all.
        datas = cursor.fetchall()
        connection.close()
        return datas

    def getJson(self, table):
        results = self.getData(table)
        data = json.dumps(results)
        return data

    def getTables(self):
        conn = sqlite3.connect(self.sqlite)
        c = conn.cursor()
        c.execute('select name from sqlite_master where type="table"')
        tables = [table[0] for table in c]
        conn.close()
        return tables

    def dumpData(self):
        d = {}
        tables = self.getTables()
        for index, table in enumerate(tables):
            data = self.getData(table)
            d[table] = data
        d.update(result='success')
        return d

    def dumpJson(self):
        data = self.dumpData()
        data = json.dumps(data)
        return data

    def setData(self, datas):
        try:
            conn = sqlite3.connect(self.sqlite)
            c = conn.cursor()
            if datas['method'] is 'insert':
                c.execute('insert into {table} (id) values ({_id})'.format(
                            table=datas['table'], _id=datas['id']))
            for key, value in datas['values'].items():
                c.execute('update {table} set {col}="{value}" where id={_id}'.format(
                            table=datas['table'], col=key, value=value, _id=datas['id']))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False


class dbManager(Daemon):
    def safeExecute(self, default, exception, function, *args):
        try:
            return True, function(*args)
        except exception:
            return False, default

    def confirmQuery(self, query):
        result, data = self.safeExecute(
                                '{"result": "wrong format of json"}',
                                ValueError, json.loads, query)
        if not result:
            return data

        method = data.get('method')
        if not method:
            data = '{"result": "no method data"}'

        elif method == 'get':
            data = self.getMethod(data)

        elif method == 'dump':
            self.updateDB()
            data = DATABASE
            data.update(result='success')
            data = json.dumps(data)

        elif method == 'set':
            LOCK.acquire()
            data = self.setMethod(data)
            LOCK.release()

        elif method == 'check':
            data = dict(result=DB_CHANGED)
            data = json.dumps(data)

        elif method == 'update':
            _mlis_dir = '/opt/mlis'
            _web_console_dir = _mlis_dir + '/web_console'

            _reboot = _web_console_dir + '/reboot.sh'
            _update_all = _mlis_dir + '/web-update-all.sh'
            _reset_dflt = _web_console_dir + '/reset_to_default.sh'
            try:
                _act = data.get('values')
                if _act == 'save_to_reset':
                    LOCK.acquire()
                    os.system('cp -f /tmp/app.db /tmp/app.db.bak')
                    result = os.system('source ' + _update_all)
                    LOCK.release()
                    if result is 0:
                        os.system(_reboot)
                        data.update(result='success')
                    else:
                        data.update(result='error')
                        data.update(values=_update_all)

                elif _act == 'reset_to_default':
                    LOCK.acquire()
                    result = os.system(_reset_dflt)
                    LOCK.release()
                    if result is 0:
                        os.system(_reboot)
                        data.update(result='success')
                    else:
                        data.update(result='error')

                else:
                    data = self.updateDB()

                data = json.dumps(data)
            except:
                data = self.updateDB()

        else:
            data = '{"result": "method error"}'

        return data

    def updateDB(self):
        global DATABASE
        LOCK.acquire()
        DATABASE = {}
        for db in DBs:
            if os.path.exists(db):
                sqldb = sqlite(db)
                DATABASE.update(sqldb.dumpData())
        LOCK.release()
        return '{"result": "DATABASE updated"}'

    def locateTable(self, table):
        for idx, db in enumerate(DBs):
            if not os.path.exists(db):
                continue
            sqldb = sqlite(db)
            if table in sqldb.getTables():
                locate = vars(sqldb)
                return locate['sqlite']

    def setMethod(self, query):
        global DATABASE
        db = self.locateTable(query.get('table'))
        if not db:
            return '{"result": "no such table"}'

        db = sqlite(db)
        table = query.get('table')
        _id = query.get('id')
        values = query.get('values')

        if not _id:
            return '{"result": "lost id table"}'

        if not values or type(values) is not dict:
            return '{"result": "wrong format of values"}'

        # if len(DATABASE[table]) < _id:
        if not len([item for item in DATABASE[query['table']] if item.get('id')==_id]):
            # return '{"result": "wrong id"}'
            query['method'] = 'insert'

        # check from here
        confirm = db_confirm()
        _bool, query = confirm.confirm(query)
        if not _bool:
            return '{"result": "illegal value."}'

        if not db.setData(query):
            return '{"result": "wrong values"}'

        try:
            if query['method'] == 'insert':
                DATABASE[query['table']].append({'id': _id})
            [item for item in DATABASE[query['table']] if item.get('id')==_id][0].update(values)
        except Exception as e:
            return '{"result": "'+str(e)+'"}'
        data = '{"result": "success"}'
        global DB_CHANGED
        DB_CHANGED = True
        return data

    def getMethod(self, query):
        data = DATABASE.get(query['table'])
        if data:
            data = {query['table']: data, 'result': 'success'}
            data = json.dumps(data)
        else:
            data = '{"result": "no such table"}'
        return data

    def run(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if os.path.exists(db_sock):
            os.remove(db_sock)
        sock.bind(db_sock)
        sock.listen(2)

        self.dbUpdate = dbUpdate()
        self.dbUpdate.daemon = True
        self.dbUpdate.start()

        while True:
            conn, addr = sock.accept()
            query = conn.recv(4096)
            data = self.confirmQuery(query)

            try:
                conn.send(data)
                conn.shutdown(2)
            except:
                pass
            conn.close()


if __name__ == "__main__":
    daemon = dbManager(pidfile)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
