#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(250, 150)
        self.center()
        self.setWindowTitle('MLiS')

        # le = QLineEdit()
        # le.setObjectName("host")
        # le.setText("Host")

        self.button1 = QtGui.QPushButton('Test', self)
        self.button1.clicked.connect(self.handleButton)
        self.button2 = QtGui.QPushButton('Quit', self)
        self.button2.clicked.connect(self.quitButton)
        self.button1.resize(50, 50)
        self.button1.move(50, 10)
        self.button2.resize(100, 50)
        self.button2.move(100, 50)

        self.show()

    def handleButton(self):
        print ('Hello World')

    def quitButton(self):
        print ('Quit')
        # sys.exit(0)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
