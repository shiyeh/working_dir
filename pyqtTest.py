#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import paramiko
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time

VERSION = u'1.0'
port = int(22)
username = u'admin'
passwd = u'1234'
rootPwd = u'G420x'
HOST = u'10.0.10.1'
_admin_home = u'/home/admin/'
_mlis_dir = u'/opt/mlis/'

SRC_FILE_LIST = ['update-fw-process.py',
                 'update-fw-check.py',
                 'update-fw-check.sh',
                 'update-fw-process.sh',
                 'db_sender.py',
                 ]


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
        self.editBox1.setText(HOST)     # Default IP
        self.editBox1.setFixedWidth(_editbox_fix_width)

        self.label2 = QtGui.QLabel(u'Password:')
        self.label2.setFixedWidth(_label_fix_width)

        self.editBox2 = QLineEdit(passwd)       # Default password
        self.editBox2.setEchoMode(self.editBox2.Password)
        self.editBox2.setFixedWidth(_editbox_fix_width)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # self.buttonBox.layout().setDirection(QtGui.QBoxLayout.RightToLeft)

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
        print(_ip_addr)
        print(_passwd)

        try:
            change_profile(_ip_addr, _passwd)
            uploadFile(_ip_addr, _passwd)
        except Exception as e:
            showError(e)
            self.close()

    def _clickCancel(self):
        self.close()


def showError(e):
    mb = QtGui.QMessageBox("ERROR", str(e), QtGui.QMessageBox.Critical,
                           QtGui.QMessageBox.Ok, 0, 0
                           )
    mb.exec_()
    return


def showInfo():
    mb = QtGui.QMessageBox("INFO", "Successful !", QtGui.QMessageBox.Information,
                           QtGui.QMessageBox.Ok, 0, 0
                           )
    mb.exec_()
    return


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
        showError(e)
        # clientExit()
        # print(e)
    else:
        pass
    finally:
        s.close()


def uploadFile(_ip_addr, _passwd):
    host = _ip_addr
    passwd = _passwd

    # paramiko.util.log_to_file('paramiko.log')
    try:
        for _SRC_File in SRC_FILE_LIST:
            remotepath = _admin_home + _SRC_File

            # For windows, get the stored path
            if hasattr(sys, "_MEIPASS"):
                localpath = os.path.join(sys._MEIPASS, _SRC_File)
            else:
                localpath = './' + _SRC_File

            paramiko.SSHClient().set_missing_host_key_policy(paramiko.AutoAddPolicy())
            scp = paramiko.Transport((host, port))
            scp.connect(username=username, password=passwd)
            sftp = paramiko.SFTPClient.from_transport(scp)
            sftp.put(localpath, remotepath)

    except Exception as e:
        showError(e)
        # clientExit()
    else:
        clear(_ip_addr, _passwd)
        print('Success !')
        showInfo()
    finally:
        scp.close()


def clear(_ip_addr, _passwd):
    host = _ip_addr
    passwd = _passwd

    print('************ !')

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

    _cmd_backup_profile = 'mv {0}.profile.4cli {0}.profile'.format(_admin_home)

    try:
        # paramiko.util.log_to_file('paramiko.log')
        print(host)
        print(username)
        print(passwd)
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, username=username, password=passwd, timeout=10)

        if username != 'root':
            ssh = s.invoke_shell()
            time.sleep(0.1)
            ssh.send('su -\n')
            buff = ''

            while not buff.endswith('Password: '):
                resp = ssh.recv(9999)
                buff += resp

            ssh.send(rootPwd)
            ssh.send('\n')
            buff = ''

            while not buff.endswith(':~# '):
                resp = ssh.recv(9999)
                buff += resp

            _cmd_rm_log = 'rm -f /opt/log/fwUpdate*.log'
            ssh.send(_cmd_rm_log)
            ssh.send('\n')
            buff = ''

            while not buff.endswith(':~# '):
                resp = ssh.recv(9999)
                buff += resp

            ssh.send(_mv_to_mlb_dir)
            ssh.send('\n')
            buff = ''

            while not buff.endswith(':~# '):
                resp = ssh.recv(9999)
                buff += resp

            ssh.send(_cmd_chown)
            ssh.send('\n')
            buff = ''

            while not buff.endswith(':~# '):
                resp = ssh.recv(9999)
                buff += resp

            ssh.send(_cmd_chmod)
            ssh.send('\n')
            buff = ''

            while not buff.endswith(':~# '):
                resp = ssh.recv(9999)
                buff += resp

        stdin, stdout, stderr = s.exec_command(_cmd_backup_profile)

    except Exception as e:
        showError(e)
        # clientExit()
    else:
        pass
    finally:
        s.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
