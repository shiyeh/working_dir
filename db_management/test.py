#!/usr/bin/python

import socket
import sys
import pprint
import json
import time
import copy


D = {"method": "set",
     "table": "system_info",
     "id": 1,
     "values": {
         "up_time": time.time(), }}

D1 = {"method": "set",
      "table": "system_info",
      "id": 1,
      "values": {
        'device_name': "TS",
        "up_time": time.time(),
        'utc_offset': '+12:00', }}

SAVE_TO_RST = {"method": "update",
               "values": "save_to_reset", }

RST_TO_DFLT = {"method": "update",
               "values": "reset_to_default", }

def send(data):
    print data
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/db.sock")
    s.send(data)
    data = s.recv(10240)
    data = json.loads(data)
    pprint.pprint(data)


def sendSet():
    querysends = []
    try:
        with open('/tmp/g420x.json', 'r') as json_file:
            data = json.load(json_file)

        for table, records in data.items():
            if type(records) is list:
                query = {'method': 'set'}
                query['table'] = table
                query['values'] = {}
                for record in records:
                    for key, value in record.items():
                        if key == 'id':
                            query['id'] = value
                        else:
                            query['values'][key] = \
                                value if str(value) != 'None' else None
                    querys.append(copy.deepcopy(query))
    except Exception as e:
        print(e)
        return '{"result": "import file not found under /tmp"}'

    print(json.dumps(querys, indent=2))
    for query in querys:
        print('------------------------------------------')
        print(query['table'])
        send(json.dumps(query))


def sendGetEx1():
    ex_table_name = 'com_setting'
    jsondata = sendGet(ex_table_name)

    for item in jsondata[ex_table_name]:
        print item["work_mode"]
        print item["trans_mode"]
        print item["baud_rate"]
        print item["parity"]
        print item["data_bits"]
        print item["stop_bits"]
        print item["ip_addr"]
        print item["port"]
        print item["service_mode"]

        if item["service_mode"] == 0:
            print "TCP client"
        elif item["service_mode"] == 1:
            print "TCP server"
        elif item["service_mode"] == 2:
            print "UDP service"


def sendGet(table):
    methods = ['dump', 'check']
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/db.sock")

    method = table if table in methods else 'get'
    send_data = '{"method": "' + method + '", "table": "' + table + '"}'

    s.send(send_data)
    print(send_data)

    data = s.recv(10240)
    data = json.loads(data)
    pprint.pprint(data)
    return data


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'save_to_reset':
            send(json.dumps(SAVE_TO_RST))
        else:
            sendGet(sys.argv[1])
        sys.exit(0)
    elif len(sys.argv) == 1:
        # print D
        # send(json.dumps(D))
        send(json.dumps(D1))
        # sendGetEx1() # demo to dump "com_setting"
        # sendSet()
    else:
        print("usage: %s name of table" % sys.argv[0])
        sys.exit(2)
