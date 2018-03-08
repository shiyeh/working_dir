#!/usr/bin/python

import os, sys
import sched, time
import logging
import sqlite3
import subprocess

# schedule = sched.scheduler(time.time, time.sleep)
log = logging.getLogger(__name__)
LOG_PATH = '/tmp/ntpd.log'


def ntp_date(server_name='pool.ntp.org'):
	log.info('Run ntpd !')
	try:
		cmd = 'ntpd -g -q ' + server_name
		subprocess.check_call(cmd.split())

		cmd = 'hwclock -w'
		subprocess.check_call(cmd.split())
	except Exception:
		print('ERROR, PASS')
		pass
	else:
		log.info('Ntpd Successful!')
		print('Success. DONE')
		sys.exit(0)
	# finally:
	# 	print('1111111111111')
	# 	sys.exit(0)


# def perform(inc=10, _ntp_server=''):
# 	schedule.enter(inc, 0, perform, (inc,))
# 	ntp_date(_ntp_server)


def main():
	# Connect to database
	# con = sqlite3.connect(os.environ["WEB_APP_DBTMP_PATH"])
	# cur = con.cursor()

	# ntpTmp = cur.execute(
	#     "select ping_addr from lan_setting;").fetchone()
	# _ntp_server = str(ntpTmp[0])
	_ntp_server_list = 'tick.stdtime.gov.tw;tock.stdtime.gov.tw;clock.stdtime.gov.tw'
	_ntp_server_list = _ntp_server_list.split(';')
	print _ntp_server_list
	# time.sleep(10)
	# _ntp_server_list = ['tick.stdtime.gov.tw',
	# 					'tock.stdtime.gov.tw',
	# 					'clock.stdtime.gov.tw']

	# con.close()

	for _ntp_server in _ntp_server_list:
		# print('ntp_server: {}'.format(_ntp_server))
		# try:
		# 	cmd = 'ping -c2 ' + _ntp_server
		# 	ret = os.system(cmd)
		# 	print('ret={}'.format(ret))
		# 	# ret = subprocess.check_call(cmd.split())

		# 	if ret != 0:
		# 		continue

		# except Exception:
		# 	print("Error command: %s" % cmd) # 'Some error occured with the command:', cmd
		# 	sys.exit(1)
		cmd = 'ping -c2 ' + _ntp_server
		ret = os.system(cmd)
		print('ret={}'.format(ret))
		# ret = subprocess.check_call(cmd.split())

		if ret != 0:
			print('PING FAILED.')
			continue
		else:
			ntp_date(_ntp_server)
			# inc = 30
			# schedule.enter(0, 0, perform, (inc, _ntp_server))
			# schedule.run()

		# time.sleep(1)


if __name__ == '__main__':
	logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
		format='%(asctime)s %(levelname)s: %(message)s')
	main()
