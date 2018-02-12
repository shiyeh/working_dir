#!/usr/bin/python

import os

_admin_home = '/home/admin/'
_mlis_dir = '/opt/mlis/'
# _tmp_file += 'update-fw-* '
# _tmp_file += '/home/admin/db_sender.py '
SRC_FILE_LIST = ['update-fw-process.py',
                 'update-fw-check.py',
                 'update-fw-check.sh',
                 'update-fw-process.sh',
                 'db_sender.py',
                 ]

_tmp = ''
for _tmp_files in SRC_FILE_LIST:
    _tmp += _admin_home
    _tmp += _tmp_files
    _tmp += ' '
_mv_to_mlb_dir = 'mv ' + _tmp + _mlis_dir

_tmp = ''
for _tmp_files in SRC_FILE_LIST:
    _tmp += _mlis_dir
    _tmp += _tmp_files
    _tmp += ' '
_cmd_chown = 'chown -R root:root ' + _tmp
_cmd_chmod = 'chmod -R 755 ' + _tmp

print _mv_to_mlb_dir
print _cmd_chown
print _cmd_chmod
