#!/usr/bin/python
# -*- coding: utf-8 -*-
import sched, time, os
import threading
import logging

log = logging.getLogger(__name__)
LOG_PATH = '/tmp/run_ntpd.log'

schedule = sched.scheduler(time.time, time.sleep)


def run_ntpd(inc):
    schedule.enter(inc, 0, run_ntpd, (inc,))
    _run_ntpd_path = '/opt/mlis/web-update-ntp-sync.py'
    os.system('/usr/bin/python {} &'.format(_run_ntpd_path))
    # Popen(['python', _run_ntpd_path], stdout=subprocess.PIPE)
    # log.debug(p.stdout.read())


def main(inc, lock):
    lock.acquire()

    # Connect to database
    # con = sqlite3.connect(os.environ["WEB_APP_DBTMP_PATH"])
    # cur = con.cursor()

    # incTmp = cur.execute(
    #     "select [[[ping_addr]]] from [[[lan_setting]]];").fetchone()
    # inc = str(incTmp[0])
    schedule.enter(0, 0, run_ntpd, (inc,))
    schedule.run()

    # con.close()
    lock.release()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
        format='%(asctime)s %(levelname)s: %(message)s')

    lock = threading.Lock()
    thread = threading.Thread(target=main, args=(30, lock))
    # thread.setDaemon(True)
    thread.start()
