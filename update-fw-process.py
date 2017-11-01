#!/usr/bin/python
import os
import sys
import logging
import time
import init_env
import subprocess
from subprocess import Popen, PIPE

log = logging.getLogger(__name__)


def clearProcess():
    ''' When update firmware finished, do the post procedure. '''
    os.chdir(os.environ['MLB_DIR'])
    try:
        subprocess.check_call(['source web-update-all.sh'], shell=True)
        log.info('Update clear and do web-update-all.sh')

    except Exception as e:
        log.exception(e)
    else:
        os.system('/bin/sync')
        os.system('/bin/sync')

    _date = time.strftime("%Y%m%d", time.localtime())
    _log_path_bak = '/opt/log/fwUpdate_{}.log'.format(_date)
    _cmd = '/bin/mv {} {}'.format(LOG_PATH, _log_path_bak)

    os.system(_cmd)
    log.info('Reboot the system.')
    os.system('/sbin/reboot')


def main():
    time.sleep(1)

    ''' Check if /tmp/mlis.tar.gz is exists. '''
    if os.path.isfile(MLIS_FILE) is False:
        log.error('{} not found'.format(MLIS_FILE))
        sys.exit(1)

    ''' Remove all files under /opt/mlis '''
    _cmd = 'rm -rf ' + os.environ['MLB_DIR'] + '/*'
    ret = os.system(_cmd)
    if ret != 0:
        log.error('Cannot remove old files.')
        sys.exit(1)
    else:
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
        log.info(out.strip())
        log.info('Finish to update firmware.')
        clearProcess()


if __name__ == '__main__':
    LOG_PATH = '/opt/log/fwUpdate.log'
    logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
                        format='%(asctime)s %(levelname)s: %(message)s')
    MLIS_FILE = '/tmp/mlis.tar.gz'

    main()
