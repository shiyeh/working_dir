#!/usr/bin/python
import os
import sys
import logging
import glob
import hashlib
import signal
import init_env
import subprocess
from subprocess import Popen, PIPE

log = logging.getLogger(__name__)


def killProcess():
    _cmd = "ps | grep {ppp_on_boot} | awk '{print $1}' | head -n 1"
    pid1 = subprocess.check_output([_cmd], shell=True)
    if pid1 == '':
        pid1 = 'Not Found'

    _cmd = 'pidof serial-config'
    p2 = Popen([_cmd], shell=True, stdout=PIPE, stderr=PIPE)
    pid2, err = p2.communicate()
    if p2.returncode != 0:
        pid2 = 'Not Found'

    for pid in [pid1, pid2]:
        log.info('Kill process: %s', pid.strip())
        try:
            os.kill(int(pid), signal.SIGTERM)
        except Exception:
            pass


def cancelProcess():
    _cmd = 'rm -f /tmp/*.fw {} {}'.format(SRCFILE, MD5FILE)
    try:
        os.system(_cmd)
    except Exception:
        pass
    finally:
        log.error('Cancel the update processes, please check your FW file.')
        sys.exit(1)


def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read()
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def main():
    ''' Get the firmware name and path. '''
    try:
        fwPath = glob.glob('/tmp/*.fw')[0]
    except Exception as e:
        log.error('Firmware not found.')
        cancelProcess()

    fwName = os.path.basename(fwPath)
    log.info('Firmware found, version is %s' % fwName)

    ''' Untar the file XXX.fw to /tmp '''
    try:
        p = Popen(['/bin/tar', '-xvpf', fwPath, '-C', '/tmp/'], stdout=PIPE, stderr=PIPE)
        fwFile, err = p.communicate()
        if p.returncode != 0:
            raise Exception(err.strip())
        # log.info('Untar the file: %s' % (fwFile))
    except Exception as e:
        log.error(e)
        cancelProcess()

    if not os.path.exists(SRCFILE) or not os.path.exists(MD5FILE):
        cancelProcess()

    ''' Try to open original md5 file, just cat file. '''
    try:
        with open(MD5FILE, 'rt') as f:
            md5_original = f.read().strip()
    except Exception as e:
        log.exception(e)
    finally:
        f.close()

    ''' Compare these 2 md5 files. '''
    md5_new = md5Checksum(SRCFILE)
    if md5_original != md5_new:
        log.error('MD5 Comparison: FAIL')
        log.error('MD5 original: %s' % (md5_original))
        log.error('MD5 NEW: %s' % (md5_new))
        log.error('Firmware update cancel because the MD5 is not the same.')
        cancelProcess()
    else:
        # Kill process before update FW.
        log.info('MD5 Comparison: PASS')
        killProcess()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/opt/log/fwUpdate.log',
                        format='%(asctime)s %(levelname)s: %(message)s')
    SRCFILE = '/tmp/mlis.tar.gz'
    MD5FILE = '/tmp/md5'
    main()
