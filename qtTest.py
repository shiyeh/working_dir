#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import paramiko
from PyQt4.QtGui import *
from PyQt4.QtCore import *


# host = '10.0.10.1'


def delLog():
    # port = 22
    username = 'root'
    passwd = 'G420x'
    _cmd = '/bin/rm /opt/log/fwUpdate*.log'
    host = ipAddr

    try:
        paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, username=username, password=passwd)
        stdin, stdout, stderr = s.exec_command(_cmd)
        # print 'OUT: ', stdout.read()
        # # print 'IN: ', stdin.read()
        # print 'ERROR: ', stderr.read()
        s.close()

    except Exception as e:
        print e
    else:
        QMessageBox.information(w, "Message", "Great!")
        QMessageBox.resize(100, 80)


def doAction():
    global ipAddr
    print 'Heloooo+{}'.format(ipAddr)


# Main window
a = QApplication(sys.argv)
w = QWidget()
w.resize(300, 160)
w.setWindowTitle("Hello world!")

label = QLabel('Where is your machine (IP address) ?', w)

# Create a button
quitButton = QPushButton('Quit', w)
quitButton.setToolTip('Click to quit')
quitButton.clicked.connect(exit)
quitButton.resize(quitButton.sizeHint())
quitButton.move(100, 80)

txt = QLineEdit('10.0.10.1', w)
txt.move(0, 20)
txt.resize(280, 25)

ipAddr = str(txt.text())

okButton = QPushButton('OK', w)
okButton.setToolTip('OK to go')
okButton.clicked.connect(delLog)
# okButton.clicked.connect(doAction)
okButton.resize(okButton.sizeHint())
okButton.move(100, 50)

# Show window
w.show()
sys.exit(a.exec_())
