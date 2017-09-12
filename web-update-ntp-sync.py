#!/usr/bin/python

import os, sys
import subprocess

try:
    cmd = 'ping -c2 www.pool.ntp.org'
    ret = subprocess.check_call(cmd.split())

    if ret == 0:
        cmd = 'ntpd -g -q pool.ntp.org'
        ret = subprocess.check_call(cmd.split())

        cmd = 'hwclock -w'
        ret = subprocess.check_call(cmd.split())

except Exception:
    # 'Some error occured with the command:', cmd
    print("Error command: %s" % cmd)
    sys.exit(1)
else:
    pass
