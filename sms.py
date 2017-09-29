#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
s = socket.socket()

ip = "10.0.10.1"
port = 10001

s = socket.socket()
s.connect((ip, port))
s.send("AT")
print s.recv(1024)
s.close()

# s.send("AT+CMEE=2")
# print s.recv(1024)

s = socket.socket()
s.connect((ip, port))
s.send("AT+CPIN?")
print s.recv(1024)
s.close()


s = socket.socket()
s.connect((ip, port))
s.send("AT+CMGF=1")
print s.recv(1024)
s.close()


s = socket.socket()
s.connect((ip, port))
s.send("AT+CMGS=\"+886《Number》\"")
print s.recv(1024)
s.close()

time.sleep(0.5)
s = socket.socket()
s.connect((ip, port))
s.send('TEST')
s.send(u'\u001A')
time.sleep(0.5)
print s.recv(1024)
s.close()
