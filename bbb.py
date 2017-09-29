#!/usr/bin/python
import socket
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipAddr = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])
    tmpList = ipAddr.split('.')
    return '{}.{}.{}'.format(tmpList[0], tmpList[1], tmpList[2])

def get_netmask(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x891b,  # SIOCGIFNETMASK
        struct.pack('256s', ifname[:15])
        )[20:24])

print get_ip_address('ens33')
# print get_netmask('ens33')

# myname = socket.getfqdn(socket.gethostname())
# myaddr = socket.gethostbyaddr(myname)
# print myname, myaddr
