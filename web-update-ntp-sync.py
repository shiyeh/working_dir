#!/usr/bin/python

import os, sys
import sched, time
import logging
import sqlite3
import subprocess

# schedule = sched.scheduler(time.time, time.sleep)
log = logging.getLogger(__name__)
LOG_PATH = '/tmp/run_ntpd.log'


def ntp_date(server_name='pool.ntp.org'):
	try:
		log.info('Run ntpd using: {}'.format(server_name))
		cmd = 'ntpd -g -q ' + server_name
		out = subprocess.check_output(cmd.split())

		cmd = 'hwclock -w'
		subprocess.check_call(cmd.split())
	except Exception:
		log.debug('Ntpd ERROR, PASS')
		pass
	else:
		log.info(out.strip())
		log.info('Time sync successful: {}'.format(server_name))
		sys.exit(0)


def main():
	# Connect to database
	# con = sqlite3.connect(os.environ["WEB_APP_DBTMP_PATH"])
	# cur = con.cursor()

	# ntpTmp = cur.execute(
	#     "select ping_addr from lan_setting;").fetchone()
	# _ntp_server = str(ntpTmp[0])
	ntpTmp = 'tick.stdtime.gov.tw;tock.stdtime.gov.tw;clock.stdtime.gov.tw'
	_ntp_server_list = ntpTmp.split(';')

	# con.close()

	for _ntp_server in _ntp_server_list:
		cmd = 'ping -c2 ' + _ntp_server
		ret = os.system(cmd)

		if ret != 0:
			log.debug('PING FAILED: {}, Try to next one.'.format(_ntp_server))
			continue
		else:
			log.info('PING Success: {}'.format(_ntp_server))
			ntp_date(_ntp_server)


if __name__ == '__main__':
	logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
		format='%(asctime)s %(levelname)s: %(message)s')
	main()
