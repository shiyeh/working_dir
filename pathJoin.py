#!/usr/bin/python
import os

SRC_FILE_LIST = ['update-fw-process.py',
                 'update-fw-check.py',
                 'update-fw-check.sh',
                 'update-fw-process.sh',
                 'db_sender.py',
                 ]
_tmp = ''
for _tmp_files in SRC_FILE_LIST:
    _tmp += '/home/admin/'
    _tmp += _tmp_files
    _tmp += ' '

print '************'
print _tmp
