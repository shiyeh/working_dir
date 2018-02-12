#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import paramiko
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

VERSION = u'1.0'
port = int(22)
username = u'admin'
passwd = u'1234'
rootPwd = u'G420x'
host = u'10.0.10.1'
_admin_home = u'/home/admin/'
_mlis_dir = u'/opt/mlis/'

# SRC_FILE_LIST = ['update-fw-process.py',
#                  'update-fw-check.py',
#                  'update-fw-check.sh',
#                  'update-fw-process.sh',
#                  'db_sender.py',
#                  ]


class MyWindow(QtGui.QWidget):
    """docstring for MyWindows"""
    def __init__(self):
        QtGui.QWidget.__init__(self)
        _label_fix_width = int(100)
        _editbox_fix_width = int(180)

        self.setWindowTitle('MLiS Update Tool v{}'.format(VERSION))
        self.resize(300, 180)
        gridlayout = QtGui.QGridLayout()

        self.label1 = QtGui.QLabel(u'IP Address:')
        self.label1.setFixedWidth(_label_fix_width)

        # IP address validator, must be 0~255
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex)

        self.editBox1 = QLineEdit()
        self.editBox1.setValidator(ipValidator)
        self.editBox1.setObjectName(u'Host')
        self.editBox1.setText(u'10.0.10.1')     # Default IP
        self.editBox1.setFixedWidth(_editbox_fix_width)

        self.label2 = QtGui.QLabel(u'Password:')
        self.label2.setFixedWidth(_label_fix_width)

        self.editBox2 = QLineEdit('1234')       # Default password
        self.editBox2.setEchoMode(self.editBox2.Password)
        self.editBox2.setFixedWidth(_editbox_fix_width)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.layout().setDirection(QtGui.QBoxLayout.RightToLeft)

        gridlayout.addWidget(self.label1, 1, 1)
        gridlayout.addWidget(self.editBox1, 1, 2)
        gridlayout.addWidget(self.label2, 2, 1)
        gridlayout.addWidget(self.editBox2, 2, 2)
        gridlayout.addWidget(self.buttonBox, 3, 2)

        self.setLayout(gridlayout)

        self.connect(self.buttonBox,
                     QtCore.SIGNAL('accepted()'),
                     self._clickOK
                     )
        self.connect(self.buttonBox,
                     QtCore.SIGNAL('rejected()'),
                     self._clickCancel
                     )

    def _clickOK(self):
        _ip_addr = str(self.editBox1.text())
        _passwd = str(self.editBox2.text())
        # print(ret1)
        # print(ret2)

        change_profile(_ip_addr, _passwd)

    def _clickCancel(self):
        self.close()


def change_profile(_ip_addr, _passwd):
    ''' When login as admin, must be change to root,
        so that change permission of /opt/mlis/
    '''
    host = _ip_addr
    passwd = _passwd

    _cp_profile_cmd1 = 'cp {0}.profile {0}.profile.4cli'.format(_admin_home)
    _cp_profile_cmd2 = 'cp {0}.profile.bak {0}.profile'.format(_admin_home)

    # paramiko.util.log_to_file('paramiko.log')
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, username=username, password=passwd, timeout=10)
        stdin, stdout, stderr = s.exec_command(_cp_profile_cmd1)
        stdin, stdout, stderr = s.exec_command(_cp_profile_cmd2)

    except Exception as e:
        # showError(e)
        # clientExit()
        print(e)
    else:
        pass
    finally:
        s.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
