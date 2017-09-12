#!/usr/bin/python
import os
import sys
import subprocess
from subprocess import Popen, PIPE

try:
    p1 = Popen(['/usr/sbin/userdel', '-r', 'admin2'], stdout=PIPE, stderr=PIPE)
    out, err = p1.communicate()

    if out:
        print 'ret> ', p1.returncode
        print 'OK> output ', out

    if err:
        print 'ret> ', p1.returncode
        print 'Error> error ', err.strip()
        raise
except OSError as e:
    print 'OSError > ', e.errno
    print 'OSError > ', e.stderr
    print 'OSError > ', e.filename

except Exception:
    print '***Error> ', sys.exc_info()[0]
finally:
    pass