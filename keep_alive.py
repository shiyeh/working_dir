#!/usr/bin/python
import os
import sys
import sqlite3
import time
import subprocess
from subprocess import Popen, PIPE
import init_env
from daemon import Daemon
import logging

log = logging.getLogger(__name__)


class KeepAlive(Daemon):
    """docstring for KeepAlive"""

    def __init__(self, lastRunTime=0, count=0):
        super(KeepAlive, self).__init__(pidfile='/tmp/keep-alive.pid')

        self.lastRunTime = lastRunTime
        self.count = count

    def _bckup_logs(self):
        logfiles_lst = ['/tmp/dev-manager.log',
                        '/tmp/mdm-manager.log',
                        '/tmp/keep-alive.log',
                        '/var/log/messages']

        # make dir with timestamp string.
        # copy log files to folder.
        _cmd = 'mkdir'
        _dstdir = '/opt/log/'
        _dstdir += 'ping-reboot-'
        _dstdir += time.strftime("%Y%m%d%H%M%S", time.localtime())
        log.debug(_cmd + ' ' + _dstdir)

        p1 = subprocess.Popen([_cmd, _dstdir], stdout=subprocess.PIPE)
        log.debug(p1.stdout.readlines())

        _cmd = 'cp'
        _dstfile = _dstdir + '/.'
        for srcfile in logfiles_lst:
            log.debug(_cmd + ' ' + srcfile + ' ' + _dstfile)
            p1 = subprocess.Popen([_cmd, srcfile, _dstfile],
                                  stdout=subprocess.PIPE)
            log.debug(p1.stdout.readlines())

    def run(self):
        try:
            # Determine what the network device is 3G or 4G
            mdm_3G = ['/dev/ttyACM0', '/dev/ttyUSB3']
            mdm_4G = '/dev/cdc-wdm1'
            nic_dev = 'no_dev'

            for _mdm in mdm_3G:
                if os.path.exists(_mdm):
                    nic_dev = 'ppp0'

            if os.path.exists(mdm_4G):
                nic_dev = 'wwan1'

            if nic_dev == 'no_dev':
                log.debug('Network device not found.')
                log.debug('Canceling keep_alive process...')
                sys.exit(1)

            _cmd = '/bin/cat'
            _txb = '/sys/class/net/' + nic_dev + '/statistics/tx_bytes'

            # Record the first tx_bytes
            oldTxBytes = subprocess.check_output([_cmd, _txb]).strip()

            while True:
                time.sleep(1)

                # Connect to database
                con = sqlite3.connect(os.environ["WEB_APP_DBTMP_PATH"])
                cur = con.cursor()

                # Reading the hostname and time interval that can be user specific
                # via web console.
                hostTmp = cur.execute(
                    "select ping_addr from lan_setting;").fetchone()
                hostName = str(hostTmp[0])

                intervalTmp = cur.execute(
                    "select ping_intvl from lan_setting;").fetchone()
                timeSpec = int(intervalTmp[0])

                # retry_count = cur.execute(
                #     "select ping_retry from lan_setting;").fetchone()
                # retry_count_spec = int(retry_count[0])
                retry_count_spec = 5

                con.close()

                # Record the current time,
                # and calcute the time interval.
                currTime = time.time()
                timeInterval = currTime - self.lastRunTime

                try:
                    '''
                    If the time gap is greater than users specify,
                    also the tx speed is less than 10k bytes per second,
                    ping the specific hostname.
                    '''
                    if timeInterval >= timeSpec:
                        # Record the New tx_bytes
                        newTxBytes = subprocess.check_output([_cmd, _txb]).strip()

                        # Calculate TX speed: kB/s
                        txSpeed = (int(newTxBytes) - int(oldTxBytes)) / 1024.0 / timeSpec

                        # If the speed <= 1 kB/s, do ping
                        if txSpeed <= 1:
                            log.debug('Detect the TX speed less than 1 kbytes.')

                            _cmd_ping = 'ping -c2 ' + hostName
                            _p_sub = subprocess.Popen(_cmd_ping.split(), stdout=PIPE, stderr=PIPE)
                            out, err = _p_sub.communicate()
                            if _p_sub.returncode != 0:
                                raise Exception

                        self.lastRunTime = time.time()
                        oldTxBytes = newTxBytes
                    else:
                        continue

                except Exception:
                    """ If ping failed count to specified number, reboot the system. """
                    self.count += 1
                    log.debug('Ping failed, Count = ' + str(self.count))
                    log.debug(out.strip())

                    if self.count >= retry_count_spec:
                        log.debug('Count to ' + str(self.count) + ', reboot the system.')
                        self._bckup_logs()
                        os.system('/sbin/reboot')
                        sys.exit(1)
                else:
                    log.info('Ping {} successful.'.format(hostName))
                    log.info(out.strip())
                    self.count = 0

        except Exception:
            log.exception('Keep_alive is not run.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/tmp/keep-alive.log',
                        format='%(asctime)s %(message)s')

    p = KeepAlive()
    p.start()
