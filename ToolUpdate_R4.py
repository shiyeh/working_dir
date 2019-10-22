#!/usr/bin/env python
# -*- coding:<utf-8> -*-
import os.path
import time
from Tkinter import *
from ttk import *
import tkMessageBox
import paramiko

port = int(22)
username = u'admin'
passwd = u'1234'
rootPwd = u'G420x'
host = u'10.0.10.1'
_admin_home = u'/home/admin/'
_mlis_dir = u'/opt/mlis/'

SRC_FILE_LIST = ['update-fw-process.py',
                 'update-fw-check.py',
                 'update-fw-check.sh',
                 'update-fw-process.sh',
                 'db_sender.py',
                 ]


def showInfo():
    tkMessageBox.showinfo('Info', 'Success !!!')


def showError(e):
    tkMessageBox.showerror('Error', 'Could not access !\n {}'.format(e))


def clientExit():
    win.destroy()


def change_profile():
    ''' When login as admin, must be change to root,
        so that change permission of /opt/mlis/
    '''
    host = entry1.get()
    passwd = entry2.get()

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
        clientExit()
    else:
        pass
    finally:
        s.close()


def clear():
    host = entry1.get()
    passwd = entry2.get()

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
        clientExit()
    else:
        pass
    finally:
        s.close()


def uploadFile():
    change_profile()

    host = entry1.get()
    passwd = entry2.get()

    # paramiko.util.log_to_file('paramiko.log')
    try:
        for SRC_File in SRC_FILE_LIST:
            remotepath = _admin_home + SRC_File

            # For windows, get the stored path
            if hasattr(sys, "_MEIPASS"):
                localpath = os.path.join(sys._MEIPASS, SRC_File)
            else:
                localpath = './' + SRC_File

            paramiko.SSHClient().set_missing_host_key_policy(paramiko.AutoAddPolicy())
            scp = paramiko.Transport((host, port))
            scp.connect(username=username, password=passwd)
            sftp = paramiko.SFTPClient.from_transport(scp)
            sftp.put(localpath, remotepath)

    except Exception as e:
        showError(e)
        clientExit()
    else:
        clear()
        print('Success !')
        showInfo()
    finally:
        scp.close()


if __name__ == '__main__':

    win = Tk()
    win.title("MLiS")
    # win.geometry('300x100')
    win.resizable(0, 0)

    space0 = Label(win, text="", width=3)
    space0.grid(row=0, column=0)

    label1 = Label(win, text="IP address:")
    label1.grid(row=0, column=1, sticky=E)
    entry1 = Entry(win, width=10)
    entry1.insert(10, host)   # Default IP: 10.0.10.1
    entry1.grid(row=0, column=3, sticky=W)

    space1 = Label(win, text="", width=1)
    space1.grid(row=0, column=2)

    label2 = Label(win, text="Password:")
    label2.grid(row=1, column=1, sticky=E)
    entry2 = Entry(win, show='*', width=10)
    entry2.insert(10, u'')
    entry2.grid(row=1, column=3, sticky=W)

    space2 = Label(win, text="", width=3)
    space2.grid(row=0, column=4)

    spaceRow = Label(win, text="", width=3)
    spaceRow.grid(row=2, column=0)

    uploadButton = Button(win, text="OK", command=uploadFile)
    uploadButton.grid(row=3, column=1, sticky=E)

    quitButton = Button(win, text="Quit", command=clientExit)
    quitButton.grid(row=3, column=3, sticky=W)
    win.mainloop()
