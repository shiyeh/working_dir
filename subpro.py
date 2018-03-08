#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-07 01:49:45
# @Author  : Leo Yeh (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import time, sys
import subprocess
import logging
from subprocess import Popen, PIPE

logging.basicConfig(level=logging.NOTSET, filename='/tmp/subpro.log',
                    format='%(asctime)s %(levelname)s \n%(message)s')
log = logging.getLogger(__name__)

_host = '8.8.8.7'
_cmd = 'ping -c2 ' + _host
count = 0
lastRunTime = 0
timeSpec = 5


while True:
    time.sleep(1)
    currTime = time.time()
    timeInterval = currTime - lastRunTime
    print('{} : {}'.format(timeInterval, timeSpec))
    try:
        if timeInterval >= timeSpec:
            print('RUN PING.')
            # out = subprocess.check_output(_cmd.split(), stderr=subprocess.STDOUT)
            p = subprocess.Popen(_cmd.split(), stdout=PIPE, stderr=PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                raise Exception
            lastRunTime = time.time()
        else:
            continue
    except Exception:
        count+=1
        print('PING FAILD: count:{}'.format(count))
        log.debug('EXCEPTION:{}'.format(out))

        if count >= 8:
            print('HAHAHA')
            sys.exit(1)
    else:
        # print('OUT: {}'.format(p))
        log.info(out.strip())
        count = 0

    # print('Count={}'.format(count))
