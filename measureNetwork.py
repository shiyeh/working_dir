#!/usr/bin/python

'''
 _______     ______
|_   _\ \   / / ___|
  | |  \ \ / /\___ \
  | |   \ V /  ___) |
  |_|    \_/  |____/
Teske Virtual System
Made by Lucas Teske
This script reads /proc/net/dev using tools.py to get the data.
The average TX/RX Rates are calculated using an Low Pass Complementary Filter with k
configured as AVG_LOW_PASS. Default to 0.2
This should output something like this on your console:
eth0: in B/S
    RX - MAX: 0 AVG: 0 CUR: 0
    TX - MAX: 0 AVG: 0 CUR: 0
lo: in B/S
    RX - MAX: 1972 AVG: 0 CUR: 0
    TX - MAX: 1972 AVG: 0 CUR: 0
wlan0: in B/S
    RX - MAX: 167658 AVG: 490 CUR: 188
    TX - MAX: 3648202 AVG: 386 CUR: 424
vmnet1: in B/S
    RX - MAX: 0 AVG: 0 CUR: 0
    TX - MAX: 0 AVG: 0 CUR: 0
'''

import time
import sys
import os
import sqlite3
import init_mlb_env


def printHelp():
    print('''
Usage:
$ python {0} <interface> \n
Ex:
$ python {0} eth0

        '''.format(sys.argv[0]))

    sys.exit(1)


def updateTraffic(tx_bytes, rx_bytes):
    con = sqlite3.connect(WEB_APP_DB_PATH)
    cur = con.cursor()
    lastRowID = cur.execute("SELECT MAX(id) FROM traffic;").fetchone()[0]
    # cur.execute("update traffic set tx=(?), rx=(?), nowTime=(?) where id=(?);", (
    #             tx_bytes, rx_bytes, nowTime, lastRowID))
    cur.execute("UPDATE traffic SET tx=(?), rx=(?), sqltime=CURRENT_TIMESTAMP WHERE id=(?);", (
                tx_bytes, rx_bytes, lastRowID))
    # cur.execute("UPDATE traffic SET tx=(?), rx=(?);", (
    #             tx_bytes, rx_bytes))
    con.commit()
    con.close()


def insertTraffic(tx_bytes, rx_bytes):
    con = sqlite3.connect(WEB_APP_DB_PATH)
    cur = con.cursor()
    # lastRowID = cur.execute("SELECT MAX(id) FROM traffic;").fetchone()[0]
    # cur.execute("insert into traffic(ID,tx,rx,nowTime) values(?,?,?,?);", (
    #             lastRowID+1, tx_bytes, rx_bytes, nowTime))
    cur.execute("INSERT INTO traffic(tx, rx, sqltime) VALUES(?, ?, CURRENT_TIMESTAMP);", (tx_bytes, rx_bytes))
    con.commit()
    con.close()


def queryLastTraffic():
    con = sqlite3.connect(WEB_APP_DB_PATH)
    cur = con.cursor()
    lastRowID = cur.execute("SELECT MAX(id) FROM traffic;").fetchone()[0]
    lastTx = cur.execute("SELECT * FROM traffic WHERE id=(?)", (lastRowID,)).fetchone()[1]
    lastRx = cur.execute("SELECT * FROM traffic WHERE id=(?)", (lastRowID,)).fetchone()[2]
    con.close()

    return int(lastTx), int(lastRx)


def resetTable():
    con = sqlite3.connect(WEB_APP_DB_PATH)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS traffic;")
    cur.execute("CREATE TABLE traffic(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
tx INT NOT NULL, \
rx INT NOT NULL, \
sqltime TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')) NOT NULL);")
    cur.execute("INSERT INTO traffic(tx, rx) VALUES(0, 0);")
    con.commit()
    con.close()

    return 0


def getNetworkInterfaces():
    ifaces = []
    with open(NIC_FILE) as f:
        data = f.read()

    data = data.split("\n")[2:]
    # print data
    # print '*******'

    # if not sys.arD! {}'.format(sys.argv[1])

    # for i in data:
    #     if i.find(sys.argv[1]) > 0:
    #         pass
    #     else:
    #         data.remove(i)

    # print 'data=', data

    # print '*****\n', i
    for i in data:
        if len(i.strip()) > 0:
            x = i.split()
            # Interface |                        Receive                          |                         Transmit
            #   iface   | bytes packets errs drop fifo frame compressed multicast | bytes packets errs drop fifo frame compressed multicast
            k = {
                "interface": x[0][:len(x[0]) - 1],
                "rx": {
                    "bytes": int(x[1]),
                    "packets": int(x[2]),
                    "errs": int(x[3]),
                    "drop": int(x[4]),
                    "fifo": int(x[5]),
                    "frame": int(x[6]),
                    "compressed": int(x[7]),
                    "multicast": int(x[8])
                },
                "tx": {
                    "bytes": int(x[9]),
                    "packets": int(x[10]),
                    "errs": int(x[11]),
                    "drop": int(x[12]),
                    "fifo": int(x[13]),
                    "frame": int(x[14]),
                    "compressed": int(x[15]),
                    "multicast": int(x[16])
                }
            }
            ifaces.append(k)
    return ifaces


def main():
    ifaces = {}

    print "Loading Network Interfaces"
    idata = getNetworkInterfaces()
    print "Filling tables"
    for eth in idata:
        ifaces[eth["interface"]] = {
            "rxrate": 0,
            "txrate": 0,
            "avgrx": 0,
            "avgtx": 0,
            "toptx": 0,
            "toprx": 0,
            "sendbytes": eth["tx"]["bytes"],
            "recvbytes": eth["rx"]["bytes"]
        }

    initTime = time.time()

    # con = sqlite3.connect(WEB_APP_DB_PATH)
    # cur = con.cursor()
    # lastRowID = cur.execute("select max(id) from traffic;").fetchone()[0]
    # if lastRowID == 0:
    #     cur.execute("insert into traffic(id, tx, rx) values(?, 0, 0);", (lastRowID+1,))
    # else:
    #     lastTx, lastRx = queryLastTraffic()
    #     cur.execute("insert into traffic(id, tx, rx) values(?, ?, ?);", (lastRowID+1, lastTx, lastRx))
    # con.commit()
    # con.close()

    lastTx, lastRx = queryLastTraffic()

    while True:
        idata = getNetworkInterfaces()
        for eth in idata:
            #   Calculate the Rate
            ifaces[eth["interface"]]["rxrate"] = (eth["rx"]["bytes"] - ifaces[eth["interface"]]["recvbytes"]) / INTERVAL
            ifaces[eth["interface"]]["txrate"] = (eth["tx"]["bytes"] - ifaces[eth["interface"]]["sendbytes"]) / INTERVAL

            #   Set the rx/tx bytes
            ifaces[eth["interface"]]["recvbytes"] = eth["rx"]["bytes"]
            ifaces[eth["interface"]]["sendbytes"] = eth["tx"]["bytes"]

            #   Calculate the Average Rate
            ifaces[eth["interface"]]["avgrx"] = int(ifaces[eth["interface"]]["rxrate"] * AVG_LOW_PASS +
                                                    ifaces[eth["interface"]]["avgrx"] * (1.0 - AVG_LOW_PASS))
            ifaces[eth["interface"]]["avgtx"] = int(ifaces[eth["interface"]]["txrate"] * AVG_LOW_PASS +
                                                    ifaces[eth["interface"]]["avgtx"] * (1.0 - AVG_LOW_PASS))

            #   Set the Max Rates
            ifaces[eth["interface"]]["toprx"] = ifaces[eth["interface"]]["rxrate"] if ifaces[eth["interface"]]["rxrate"] > ifaces[eth["interface"]]["toprx"] else ifaces[eth["interface"]]["toprx"]
            ifaces[eth["interface"]]["toptx"] = ifaces[eth["interface"]]["txrate"] if ifaces[eth["interface"]]["txrate"] > ifaces[eth["interface"]]["toptx"] else ifaces[eth["interface"]]["toptx"]

            # Uncomment if needed
            # print "%s: in B/S" % (eth["interface"])
            # print "\tRX - MAX: %s AVG: %s CUR: %s" % (ifaces[eth["interface"]]["toprx"], ifaces[eth["interface"]]["avgrx"], ifaces[eth["interface"]]["rxrate"])
            # print "\tTX - MAX: %s AVG: %s CUR: %s" % (ifaces[eth["interface"]]["toptx"], ifaces[eth["interface"]]["avgtx"], ifaces[eth["interface"]]["txrate"])

            print "{}:".format(eth["interface"])
            print "  RX - recvbytes: {} bytes".format(ifaces[eth["interface"]]["recvbytes"])
            print "  TX - sendbytes: {} bytes".format(ifaces[eth["interface"]]["sendbytes"])
            print ""

            ''' Insert/update all tx/rx bytes '''
            if eth["interface"] == wanInterface:
                print 'This is {}.'.format(eth["interface"])
                updateTraffic(ifaces[eth["interface"]]["sendbytes"]+lastTx,
                              ifaces[eth["interface"]]["recvbytes"]+lastRx,
                              )

                currTime = time.time()
                timeInterval = currTime - initTime
                if timeInterval >= record_intvl:
                    insertTraffic(ifaces[eth["interface"]]["sendbytes"]+lastTx,
                                  ifaces[eth["interface"]]["recvbytes"]+lastRx,
                                  )
                    initTime = time.time()

        time.sleep(INTERVAL)


if __name__ == '__main__':
    INTERVAL = 3            # seconds
    AVG_LOW_PASS = 0.2      # Simple Complemetary Filter

    NIC_FILE = "/proc/net/dev"
    wanInterface = 'lo'
    WEB_APP_DB_PATH = os.environ["WEB_APP_DBTMP_PATH"]

    # Every 'record_intvl' seconds, insert new data to the table,
    # default is 1 hour.
    # record_intvl = 3600
    record_intvl = 20

    if len(sys.argv) == 2 and sys.argv[1] == 'reset':
        if resetTable() == 0:
            print 'Reset table...'
            sys.exit(0)

    if not os.path.exists(WEB_APP_DB_PATH):
        print 'DB not found'
        sys.exit(1)

    main()
