#!/usr/bin/python

import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE


def do():
    print 'Do ping.'


def main():
    # currTime = time.time()
    # timeInterval = currTime - lastPingTime
    # mdm_3G = '/dev/ttyACM0'
    # mdm_4G = '/dev/cdc-wdm1'

    # print os.path.exists(mdm_3G)
    # print os.path.exists(mdm_4G)
    # if os.path.exists(mdm_3G):
    #     dev = 'ppp0'
    #     print 'dev=', dev
    # elif os.path.exists(mdm_4G):
    #     dev = 'wwan1'
    #     print 'dev=', dev
    # else:
    #     print 'Network device not found.'
    #     sys.exit(1)

    dev = 'ens33'
    _cmd = '/bin/cat'
    _txp = '/sys/class/net/{}/statistics/tx_bytes'.format(dev)

    oldTxPkt = int(subprocess.check_output([_cmd, _txp]).strip())
    print oldTxPkt
    # txPackets = p1.communicate()[0].strip()
    # txList[0] = txPackets
    time1 = time2 = time.time()
    print time1
    print time2

    while True:
        print 'oldTxPkt=', oldTxPkt
        # p2 = Popen([_cmd, _txp], stdout=PIPE, stderr=PIPE)
        newTxPkt = int(subprocess.check_output([_cmd, _txp]).strip())

        print oldTxPkt, newTxPkt
        # Calculate transmision speed: kB/s
        speed = (newTxPkt - oldTxPkt) / 1024.0 / 2
        print('Now speed is {:.3f} kB/s'.format(speed))

        if speed <= 10:
            do()

        time.sleep(2)
        oldTxPkt = newTxPkt


if __name__ == '__main__':
    main()
