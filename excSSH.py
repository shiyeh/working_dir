#!/usr/bin/python
# -*- coding:<big5> -*-
from Tkinter import *
from ttk import *
import tkMessageBox
import paramiko

port = 22
username = 'root'
passwd = 'G420x'
# host = '10.0.10.1'


def showMessage():
    tkMessageBox.showinfo('Info', 'Success !!!')


def showError(e):
    tkMessageBox.showerror('Error', 'Could not access !')


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
        showMessage()


def clientExit():
    win.destroy()


if __name__ == '__main__':
    win = Tk()
    win.title("MLiS")
    # win.geometry('300x100')
    win.resizable(0, 0)

    label1 = Label(win, text="Where is your machime (IP address) ?")
    label1.grid(row=0, column=0, sticky=W)
    entry1 = Entry(win)
    entry1.insert(10, "10.0.10.1") # Default IP: 10.0.10.1
    entry1.grid(row=1, column=0, sticky=W)

    okButton = Button(win, text="OK", command=delLog)
    okButton.grid(row=1, column=1, sticky=W)
    quitButton = Button(win, text="Quit", command=clientExit)
    quitButton.grid(row=2, column=1, sticky=W)

    win.mainloop()
