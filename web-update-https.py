#!/usr/bin/python
import subprocess
import os


def genKeyCrt():
    sslPath = '/etc/nginx/ssl'
    if not os.path.exists(sslPath):
        os.system('/bin/mkdir -p {}'.format(sslPath))

    _cmd = '/usr/bin/openssl'
    _cmd += ' req -x509'
    _cmd += ' -nodes'
    _cmd += ' -days 365'
    _cmd += ' -newkey rsa:2048'
    _cmd += ' -keyout /etc/nginx/ssl/nginx.key'
    _cmd += ' -out /etc/nginx/ssl/nginx.crt'
    _cmd += ' -config /home/root/openssl.cnf'
    return subprocess.check_call([_cmd], shell=True)


def main():
    genKeyCrt()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.NOTSET, filename='/opt/log/addUser.log',
    #                     format='%(asctime)s %(levelname)s: %(message)s')
    main()
