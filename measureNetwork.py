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

# INTERVAL = 3            # seconds
# AVG_LOW_PASS = 0.2      # Simple Complemetary Filter

# nicFile = "/proc/net/dev"
# nicName = "ens33"


def printHelp():
    print('''
Usage:
$ python {0} <interface> \n
Ex:
$ python {0} eth0

        '''.format(sys.argv[0]))

    sys.exit(1)


def getNetworkInterfaces():
    ifaces = []
    with open(nicFile) as f:
        data = f.read()

    data = data.split("\n")[2:]
    print data
    # print '*******'

    # if not sys.arD! {}'.format(sys.argv[1])

    for i in data:
        if i.find(sys.argv[1]) > 0:
            pass
        else:
            data.remove(i)

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
        time.sleep(INTERVAL)


if __name__ == '__main__':
    INTERVAL = 3            # seconds
    AVG_LOW_PASS = 0.2      # Simple Complemetary Filter

    nicFile = "/proc/net/dev"

    if len(sys.argv) == 2:
        if '--help' == sys.argv[1]:
            printHelp()

    # Monitor loop
    main()
