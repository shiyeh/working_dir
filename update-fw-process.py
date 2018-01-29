#!/usr/bin/python
import os
import sys
import logging
import time
import init_env
import subprocess
from subprocess import Popen, PIPE

log = logging.getLogger(__name__)
LOG_PATH = '/tmp/fwUpdate.log'
MLIS_FILE = '/opt/mlis.tar.gz'
MD5_FILE = '/opt/md5'


def clearProcess():
    ''' When update firmware finished, do the post procedure. '''
    os.chdir(os.environ['MLB_DIR'])

    try:
        log.info('Update clear and do web-update-all.sh')
        _cmd = 'rm -rf ' + MLIS_FILE + ' ' + MD5_FILE
        os.system(_cmd)

        subprocess.check_call(['source web-update-all.sh'], shell=True)
    except Exception as e:
        log.exception(e)
    else:
        os.system('/bin/sync')
        os.system('/bin/sync')

    ''' Backup log file '''
    _date = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    _log_path_bak = '/opt/log/fwUpdate_{}.log'.format(_date)
    _cmd = '/bin/mv {} {}'.format(LOG_PATH, _log_path_bak)

    log.info('Reboot the system.')
    os.system(_cmd)
    os.system('/bin/sync; /sbin/reboot')


def main():
    time.sleep(1)

    ''' Check if /opt/mlis.tar.gz is exists. '''
    if os.path.isfile(MLIS_FILE) is False:
        log.error('{} not found'.format(MLIS_FILE))
        sys.exit(1)

    ''' Backup older firmware files '''
    _fw_bak_path = '/opt/mlis.old'
    if os.path.isdir(_fw_bak_path):
        _cmd = 'rm -rf ' + _fw_bak_path
        os.system(_cmd)
    _cmd = 'cp -a ' + os.environ['MLB_DIR'] + _fw_bak_path
    os.system(_cmd)

    ''' Remove older files under /opt/mlis '''
    _cmd = 'rm -rf ' + os.environ['MLB_DIR'] + '/*'
    ret = os.system(_cmd)
    if ret != 0:
        log.error('Cannot remove old files.')
        sys.exit(1)
    else:
        os.system('/bin/sync')
        os.system('/bin/sync')
        log.info('Remove all files under {}'.format(os.environ['MLB_DIR']))

    ''' Untar and do firmware update. '''
    _cmd = '/bin/tar'
    _cmd += ' -xvpf'
    _cmd += ' ' + MLIS_FILE
    _cmd += ' -C /'
    p = Popen(_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        log.error(err.strip())
        sys.exit(2)
    else:
        log.info('Untar file: {}'.format(MLIS_FILE))
        log.info(out.strip())
        log.info('Finish to update firmware.')
        clearProcess()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
