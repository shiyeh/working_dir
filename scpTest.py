#!/usr/bin/python
# -*- coding:<utf-8> -*-
import os.path
from Tkinter import *
from ttk import *
import tkMessageBox
import paramiko

port = 22
username = 'root'
passwd = 'G420x'
host = '10.0.10.1'


def showInfo():
    tkMessageBox.showinfo('Info', 'Success !!!')


def showError(e):
    tkMessageBox.showerror('Error', 'Could not access !\n {}'.format(e))


def clientExit():
    win.destroy()


def delLog():
    _cmd = '/bin/rm -f /opt/log/fwUpdate*.log'
    host = entry1.get()

    try:
        # paramiko.util.log_to_file('paramiko.log')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, username=username, password=passwd)
        stdin, stdout, stderr = s.exec_command(_cmd)
        # print 'OUT: ', stdout.read()
        # # print 'IN: ', stdin.read()
        # print 'ERROR: ', stderr.read()
        s.close()

    except Exception as e:
        showError(e)
        clientExit()
    else:
        print('Success !')
        showInfo()


def uploadFile():
    # SRC_File = 'update-fw-process.py'
    SRC_File = '123.log'

    # For windows, get the stored path
    if hasattr(sys, "_MEIPASS"):
        srcFilePath = os.path.join(sys._MEIPASS, SRC_File)
        print srcFilePath

    localpath = srcFilePath
    remotepath = '/opt/mlis/' + SRC_File
    host = entry1.get()

    try:
        # paramiko.util.log_to_file('paramiko.log')
        paramiko.SSHClient().set_missing_host_key_policy(paramiko.AutoAddPolicy())
        scp = paramiko.Transport((host, port))
        scp.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.put(localpath, remotepath)

        # stdin, stdout, stderr = s.exec_command(_cmd)
        # print 'OUT: ', stdout.read()
        # # print 'IN: ', stdin.read()
        # print 'ERROR: ', stderr.read()
        scp.close()

    except Exception as e:
        showError(e)
        clientExit()
    else:
        print('Success !')
        showInfo()


if __name__ == '__main__':
    win = Tk()
    win.title("MLiS")
    # win.geometry('300x100')
    win.resizable(0, 0)

    label1 = Label(win, text="Where is your machime (IP address) ?")
    label1.grid(row=0, column=0, sticky=W)
    entry1 = Entry(win)
    entry1.insert(10, host)   # Default IP: 10.0.10.1
    entry1.grid(row=1, column=0, sticky=W)

    uploadButton = Button(win, text="Upload", command=uploadFile)
    uploadButton.grid(row=1, column=1, sticky=W)

    okButton = Button(win, text="OK to go", command=delLog)
    okButton.grid(row=2, column=1, sticky=W)

    quitButton = Button(win, text="Quit", command=clientExit)
    quitButton.grid(row=3, column=1, sticky=W)

    win.mainloop()
