#!/usr/bin/python

import os
import sys
import sqlite3
import init_mlb_env
import logging

log = logging.getLogger(__name__)


def genNetifConf(IF_ADDR_IP, IF_MASK_STR, IF_ADDR_SUB):
    # netInterfacePath = os.environ['SYS_NETWORK_DIR'] + '/' + os.environ['MLB_NETWORK_IFACES']
    netInterfacePath = '/tmp/pawwwwwthhhh'
    print netInterfacePath

    # Generate /etc/network/interfaces file
    with open(netInterfacePath, 'w+') as f:
            tmp = '# Begin ' + netInterfacePath + '\n'
            tmp += '# The loopback interface\n'
            tmp += 'auto lo\n'
            tmp += 'iface lo inet loopback\n'
            tmp += '\n# Wired interfaces\n'
            tmp += 'auto eth0\n'
            tmp += 'iface eth0 inet static\n'
            tmp += '    address     {}\n'.format(IF_ADDR_IP)
            tmp += '    netmask     {}\n'.format(IF_MASK_STR)
            tmp += '    network     {}.0\n'.format(IF_ADDR_SUB)
            tmp += '    broadcast   {}.255\n'.format(IF_ADDR_SUB)
            tmp += '\niface wwan1 inet dhcp\n'
            tmp += '# End {}\n'.format(netInterfacePath)

            f.write(tmp)


def mask2CIDR(submask):
    # calculate mask to cidr
    return sum([bin(int(x)).count("1") for x in submask.split(".")])


def main():
    # NETWORK INTERFACE configuration.
    con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
    cur = con.cursor()

    DB_IF_ADDR_IP = cur.execute("select ip_addr from lan_setting").fetchone()[0]
    DB_IF_MASK_STR = cur.execute("select submask from lan_setting").fetchone()[0]
    IF_CIDR = mask2CIDR(DB_IF_MASK_STR)
    print IF_CIDR

    if DB_IF_ADDR_IP == '127.0.0.1':
        log.error('Not allow IP setting, {}'.format(DB_IF_ADDR_IP))
        sys.exit(1)

    IF_ADDR_SUB = '.'.join(DB_IF_ADDR_IP.split('.')[:3])
    IF_ADDR_IP = DB_IF_ADDR_IP
    IF_MASK_STR = DB_IF_MASK_STR

    print IF_ADDR_SUB
    print IF_ADDR_IP
    print IF_MASK_STR

    genNetifConf(IF_ADDR_IP, IF_MASK_STR, IF_ADDR_SUB)

    con.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/tmp/web_update_all.log',
                        format='%(asctime)s %(levelname)s: %(message)s')

    if not os.path.exists(os.environ['WEB_APP_DB_PATH']):
        log.error('Database not found, please check.')
        sys.exit(1)
    else:
        main()
