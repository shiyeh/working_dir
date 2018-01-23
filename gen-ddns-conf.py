#!/usr/bin/python

import os
import sys
import sqlite3
import logging
import init_env

log = logging.getLogger(__name__)

LOG_PATH = '/tmp/gen-ddns-conf.log'


def genDdnsConf(protocol, host, user, pwd):
    ddclient_dir_path = '/etc/ddclient/'
    ddclient_conf = ddclient_dir_path + 'ddclient.conf'

    if not os.path.isdir(ddclient_dir_path):
        os.mkdir(ddclient_dir_path)

    if protocol == 'noip':
        server = u'dynupdate.no-ip.com'
    elif protocol == 'dyndns2':
        server = u'members.dyndns.org'

    # Here is just for No-IP configuration
    with open(ddclient_conf, 'w+') as f:
        tmp = '### Generate {} ###\n'.format(ddclient_conf)
        tmp += 'daemon=300\n'
        tmp += 'syslog=yes\n'
        tmp += 'pid=/var/run/ddclient.pid\n'
        tmp += 'cache=/tmp/ddclient.cache\n'
        # Default: not ssl.
        tmp += 'ssl=no\n'
        tmp += '\n'
        tmp += 'protocol={}\n'.format(protocol)
        tmp += 'server={}\n'.format(server)
        tmp += "use=web, web=checkip.dyndns.org/, web-skip='IP Address'\n"
        tmp += 'login={}\n'.format(user)
        tmp += 'password={}\n'.format(pwd)
        tmp += '{}\n'.format(host)

        f.write(tmp)


def main():
    con = sqlite3.connect(os.environ['WEB_APP_DBTMP_PATH'])
    cur = con.cursor()

    try:
        rule = 'select active from ddns_setting where id=1'
        DDNS_ACTIVE = cur.execute(rule).fetchone()[0]

        if DDNS_ACTIVE == 0:
            log.debug('DDNS disabled.')
            return
        else:
            rule = 'select server_provider from ddns_setting where id=1'
            DDNS_PROTOCOL = cur.execute(rule).fetchone()[0]
            rule = 'select host_name from ddns_setting where id=1'
            DDNS_HOST = cur.execute(rule).fetchone()[0]
            rule = 'select username from ddns_setting where id=1'
            DDNS_UN = cur.execute(rule).fetchone()[0]
            rule = 'select password from ddns_setting where id=1'
            DDNS_PWD = cur.execute(rule).fetchone()[0]
    except Exception as e:
        log.debug(e)
    else:
        genDdnsConf(DDNS_PROTOCOL, DDNS_HOST, DDNS_UN, DDNS_PWD)
    finally:
        con.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
