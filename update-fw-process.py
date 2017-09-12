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
    '''When untar finished, do the post procedure.'''
    os.chdir(os.environ['MLB_DIR'])
    try:
        subprocess.check_call(['source web-update-all.sh'], shell=True)
        log.info('Clear, and do web-update-all.sh')

    except Exception as e:
        log.exception(e)
    else:
        os.system('/bin/sync')
        log.info('Reboot the system.')
        os.system('/sbin/reboot')
    finally:
        pass


def main():
    time.sleep(1)

    ''' Check if /tmp/mlis.tar.gz is exists. '''
    if os.path.isfile('/tmp/mlis.tar.gz') is False:
        log.error('/tmp/mlis.tar.gz not found')
        sys.exit(1)

    ''' Remove all files under /opt/mlis '''
    _cmd = 'rm -rf ' + os.environ['MLB_DIR'] + '/*'
    ret = os.system(_cmd)
    if ret != 0:
        log.error('Cannot remove old files.')
    else:
        log.info('Remove all files under %s' % os.environ['MLB_DIR'])

    ''' Untar and do firmware update. '''
    _cmd = '/bin/tar'
    _cmd += ' -xvpf'
    _cmd += '/tmp/mlis.tar.gz'
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
    logging.basicConfig(level=logging.NOTSET, filename='/opt/log/fwUpdate.log',
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
