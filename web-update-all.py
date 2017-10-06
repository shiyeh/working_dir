#!/usr/bin/python

import os
import sys
import sqlite3
import init_mlb_env
import logging

log = logging.getLogger(__name__)


def genVpnConf(VPN_IPSEC_CONF_RULES):
    # vpnConfPath = os.environ['MLB_VPN_CFG_PATH']
    vpnConfPath = '/tmp/vpn_conf'

    # Generate /opt/mlis/conf/ipsec.conf file
    with open(vpnConfPath, 'w+') as f:
        tmp = '#!/bin/sh\n'
        tmp += '# Begin ' + vpnConfPath + '\n'
        tmp += '# ipsec.conf - strongSwan IPsec configuration file\n'
        tmp += '\n'
        tmp += '# basic configuration\n'
        tmp += '\n'
        tmp += 'config setup\n'
        tmp += '        # strictcrlpolicy=yes\n'
        tmp += '        # uniqueids = no\n'
        tmp += '\n'
        tmp += '# Add connections here.\n'
        tmp += '\n'
        tmp += 'conn %default\n'
        tmp += '        mobike=no\n'
        tmp += '        keyingtries=%forever\n'
        tmp += '\n'
        tmp += VPN_IPSEC_CONF_RULES
        tmp += '# End {}\n'.format(vpnConfPath)

        f.write(tmp)


def genApnConf(PRISIM, BCKINGSIM, DB_APN, DB_USR_NAME, DB_PASS_WRD,
               DB_2ND_APN, DB_2ND_USR_NAME, DB_2ND_PASS_WRD):
    # apnConfPath = os.environ['MLB_PPP_APN_OPT_PATH']
    apnConfPath = '/tmp/apn_opt'

    # Generate /opt/mlis/conf/apn_opt file
    with open(apnConfPath, 'w+') as f:
        tmp = '#!/bin/sh\n'
        tmp += '# Begin ' + apnConfPath + '\n'
        tmp += 'export MLBPRISIM=\"' + 'sim{}\"\n'.format(PRISIM)
        tmp += 'export MLBBCKSIM=\"' + 'sim{}\"\n'.format(BCKINGSIM)
        tmp += '\n'
        tmp += 'export MLBAPN1={}\n'.format(DB_APN)
        tmp += 'export MLBPDPYTPE1=ip\n'
        tmp += 'export MLBUSRNAME1={}\n'.format(DB_USR_NAME)
        tmp += 'export MLBPASSWORD1={}\n'.format(DB_PASS_WRD)
        tmp += 'export MLBAPN2={}\n'.format(DB_2ND_APN)
        tmp += 'export MLBPDPYTPE2=ip\n'
        tmp += 'export MLBUSRNAME2={}\n'.format(DB_2ND_USR_NAME)
        tmp += 'export MLBPASSWORD2={}\n'.format(DB_2ND_PASS_WRD)
        tmp += '\n'
        tmp += '# End {}\n'.format(apnConfPath)

        f.write(tmp)


def genDhcpdConf(DHCPD_IP_START, DHCPD_IP_END, DHCP_STATIC_LEASE,
                 DB_DHCP_IP_DNS, DB_DHCP_IP_SEC_DNS, DHCP_IP_SUBMASK,
                 IF_ADDR_IP, DHCP_CLIENT_TIME):
    # dhcpdConfPath = os.environ['SYS_DIR'] + '/' + os.environ['MLB_DHCP_CFG']
    dhcpdConfPath = '/tmp/dhcpdConfPath'

    # Generate /etc/udhcpd.conf file
    with open(dhcpdConfPath, 'w+') as f:
        tmp = '# Begin {}\n'.format(dhcpdConfPath)
        tmp += '# The start and end of the IP lease block\n'
        tmp += 'start       {}\n'.format(DHCPD_IP_START)
        tmp += 'end         {}\n'.format(DHCPD_IP_END)
        tmp += '# The interface that udhcpd will use\n'
        tmp += 'interface {}\n'.format(os.environ['DHCPD_USED_IF'])
        tmp += '# The location of the pid file\n'
        tmp += 'pidfile     /var/run/udhcpd.pid\n\n'
        tmp += '# Static leases map\n'
        tmp += '{}\n\n'.format(DHCP_STATIC_LEASE)
        tmp += '''# The remainder of options are DHCP options and can be specified with the
# keyword 'opt' or 'option'. If an option can take multiple items, such
# as the dns option, they can be listed on the same line, or multiple
# lines.\n'''
        tmp += 'opt         dns     {} {} #public google dns servers\n'.format(DB_DHCP_IP_DNS, DB_DHCP_IP_SEC_DNS)
        tmp += 'option      subnet  {}\n'.format(DHCP_IP_SUBMASK)
        tmp += 'opt         router  {}\n'.format(IF_ADDR_IP)
        tmp += 'option      lease   {} # default: 10 days\n'.format(DHCP_CLIENT_TIME)
        tmp += '# Arbitrary option in hex form:\n'
        tmp += 'option      0x08    01020304 # option 8: "cookie server IP addr: 1.2.3.4"\n'
        tmp += '# The location of the leases file\n'
        tmp += 'lease_file     /var/lib/misc/udhcpd.leases\n\n'
        tmp += '# End {}\n'.format(dhcpdConfPath)

        f.write(tmp)


def genNetifConf(IF_ADDR_IP, IF_MASK_STR,
                 IF_NETWORK, IF_BROADCAST):
    # netInterfacePath = os.environ['SYS_NETWORK_DIR'] + '/' + os.environ['MLB_NETWORK_IFACES']
    netInterfacePath = '/tmp/pawwwwwthhhh'
    # print netInterfacePath

    # Generate /etc/network/interfaces file
    with open(netInterfacePath, 'w+') as f:
        tmp = '# Begin ' + netInterfacePath + '\n'
        tmp += '# The loopback interface\n'
        tmp += 'auto lo\n'
        tmp += 'iface lo inet loopback\n'
        tmp += '\n# Wired interfaces\n'
        tmp += 'auto eth0\n'
        tmp += 'iface eth0 inet static\n'
        tmp += '    address     {}\n'.format(IF_ADDR_IP)
        tmp += '    netmask     {}\n'.format(IF_MASK_STR)
        tmp += '    network     {}\n'.format(IF_NETWORK)
        tmp += '    broadcast   {}\n'.format(IF_BROADCAST)
        tmp += '\niface wwan1 inet dhcp\n'
        tmp += '# End {}\n'.format(netInterfacePath)

        f.write(tmp)


def mask2CIDR(submask):
    # Calculate netmask to CIDR.
    return sum([bin(int(x)).count("1") for x in submask.split(".")])


def main():
    ''' NETWORK INTERFACE configuration. '''
    con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
    cur = con.cursor()

    DB_IF_ADDR_IP = cur.execute("select ip_addr from lan_setting").fetchone()[0]
    DB_IF_MASK_STR = cur.execute("select submask from lan_setting").fetchone()[0]
    IF_CIDR = mask2CIDR(DB_IF_MASK_STR)
    print 'IF_CIDR=', IF_CIDR

    if DB_IF_ADDR_IP == '127.0.0.1':
        log.error('Not allow IP setting, {}'.format(DB_IF_ADDR_IP))
        sys.exit(1)

    tmp = []
    tmp = DB_IF_ADDR_IP.split('.')
    tmp[3] = u'0'
    IF_NETWORK = '.'.join(tmp) # Should be 10.0.10.0
    tmp[3] = u'255'
    IF_BROADCAST = '.'.join(tmp) # Should be 10.0.10.255

    IF_ADDR_IP = DB_IF_ADDR_IP
    IF_MASK_STR = DB_IF_MASK_STR

    # print 'IF_ADDR_IP=',IF_ADDR_IP
    # print 'IF_MASK_STR=',IF_MASK_STR
    # print 'IF_NETWORK=',IF_NETWORK
    # print 'IF_BROADCAST=',IF_BROADCAST

    genNetifConf(IF_ADDR_IP, IF_MASK_STR,
                 IF_NETWORK, IF_BROADCAST)

    ''' DHCP SEVER configuration. '''
    DB_DHCP_EN = cur.execute("select dhcp_server from dhcp_server").fetchone()[0]
    DB_DHCPD_IP_START = cur.execute("select start_ip from dhcp_server").fetchone()[0]
    DB_DHCP_IP_SUBMSK = cur.execute("select submask from dhcp_server").fetchone()[0]
    DB_DHCP_IP_DNS = cur.execute("select dns from dhcp_server").fetchone()[0]
    DB_DHCP_IP_SEC_DNS = cur.execute("select sec_dns from dhcp_server").fetchone()[0]
    DB_DHCP_IP_RANGE = cur.execute("select max_users from dhcp_server").fetchone()[0]
    DHCP_CLIENT_TIME = cur.execute("select client_time from dhcp_server").fetchone()[0]

    DHCP_IP_RNG_START = DB_DHCPD_IP_START.split('.')[3]
    DHCP_IP_RNG_END = str(int(DHCP_IP_RNG_START) + int(DB_DHCP_IP_RANGE) - 1)
    DHCPD_IP_START = DB_DHCPD_IP_START

    tmp = []
    tmp = DB_IF_ADDR_IP.split('.')
    tmp[3] = DHCP_IP_RNG_END
    DHCPD_IP_END = '.'.join(tmp)

    DHCP_IP_SUBMASK = DB_DHCP_IP_SUBMSK

    DHCP_STATIC_LEASE = ''
    for indx in xrange(1, 6):
        DB_DHCP_STATIC_EN = cur.execute("select active from dhcp_mapping where id=(?);", (indx,)).fetchone()[0]
        if DB_DHCP_STATIC_EN == 1:
            DB_DHCP_STC_IP = cur.execute("select ip from dhcp_mapping where id=(?);", (indx,)).fetchone()[0]
            DB_DHCP_STC_MAC = cur.execute("select mac from dhcp_mapping where id=(?);", (indx,)).fetchone()[0]
            DHCP_STATIC_LEASE += 'static_lease ' + DB_DHCP_STC_IP + ' ' + DB_DHCP_STC_MAC
            DHCP_STATIC_LEASE += '\n'
            print DHCP_STATIC_LEASE

    if DB_DHCP_EN == 1:
        pass
        # _cmd = '/usr/sbin/update-rc.d -f udhcpd defaults'
        # os.system(_cmd)
    else:
        pass
        # _cmd = '/usr/sbin/update-rc.d -f udhcpd remove'
        # os.system(_cmd)

    genDhcpdConf(DHCPD_IP_START, DHCPD_IP_END, DHCP_STATIC_LEASE,
                 DB_DHCP_IP_DNS, DB_DHCP_IP_SEC_DNS, DHCP_IP_SUBMASK,
                 IF_ADDR_IP, DHCP_CLIENT_TIME)

    ''' MODEM INTERNET CONNECTION setting. '''
    PRISIM = cur.execute("select priority from wan_priority_setting where id=1;").fetchone()[0]
    if PRISIM == 1:
        BCKINGSIM = '2'
    elif PRISIM == 2:
        BCKINGSIM = '1'
    else:
        PRISIM = '1'
        BCKINGSIM = '2'

    DB_APN = cur.execute("select apn from wan_setting where id=(?);", (PRISIM,)).fetchone()[0]
    DB_USR_NAME = cur.execute("select username from wan_setting where id=(?);", (PRISIM,)).fetchone()[0]
    DB_PASS_WRD = cur.execute("select password from wan_setting where id=(?);", (PRISIM,)).fetchone()[0]
    DB_2ND_APN = cur.execute("select apn from wan_setting where id=(?);", (BCKINGSIM,)).fetchone()[0]
    DB_2ND_USR_NAME = cur.execute("select username from wan_setting where id=(?);", (BCKINGSIM,)).fetchone()[0]
    DB_2ND_PASS_WRD = cur.execute("select password from wan_setting where id=(?);", (BCKINGSIM,)).fetchone()[0]

    genApnConf(PRISIM, BCKINGSIM, DB_APN, DB_USR_NAME, DB_PASS_WRD,
               DB_2ND_APN, DB_2ND_USR_NAME, DB_2ND_PASS_WRD)

    with open(os.environ['MLB_QMI_APN_OPT_PATH'], 'w+') as f:
        f.write('APN={}\n'.format(DB_APN))

    tmpPath = os.environ['MLB_CONF_DIR'] + '/pap-secrets'
    with open(tmpPath, 'w+') as f:
        if not DB_USR_NAME and not DB_PASS_WRD:
            f.write('')
        else:
            f.write('{0}    *    {1}\n'.format(DB_USR_NAME, DB_PASS_WRD))

    ''' Ipsec VPN Setting '''
    DB_VPN_ACTIVE = cur.execute("select active from vpn_active").fetchone()[0]
    DB_VPN_POSTROUTING_INDX = ()
    VPN_IPSEC_CONF_RULES = ''
    VPN_IPSEC_SECRETS_RULES = ''

    if DB_VPN_ACTIVE == 0:
        _cmd = '/usr/sbin/update-rc.d -f ipsec remove'
        os.system(_cmd)
    else:
        for indx in xrange(1, 6):
            DB_VPN_IPSEC_EN = cur.execute("select ipsec from vpn where id=(?);", (indx,)).fetchone()[0]
            if DB_VPN_IPSEC_EN == 0:
                continue

            DB_VPN_POSTROUTING_INDX += indx
            DB_VPN_CONN_NAME = cur.execute("select conn_name from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_LEFT = cur.execute("select _left from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_START_MODE = cur.execute("select startup_mode from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_LEFT_SUBNET = cur.execute("select leftsubnet from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_LEFTID = cur.execute("select leftid from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_RIGHT = cur.execute("select _right from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_RIGHT_SUBNET = cur.execute("select rightsubnet from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_RIGHTID = cur.execute("select rightid from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_IKE_MODE = cur.execute("select keyexchange from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_OPER_MODE = cur.execute("select aggressive from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_IKE_ENCRYPT = cur.execute("select ike from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_LIFETIME = cur.execute("select lifetime from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_REKEY = cur.execute("select rekey from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_ESP = cur.execute("select esp from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_DPD_ACTION = cur.execute("select dpdaction from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_DPD_DELAY = cur.execute("select dpddelay from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_DPD_TIMEOUT = cur.execute("select dpdtimeout from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_AUTH_MODE = cur.execute("select auth_mode from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_PSK = cur.execute("select psk from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_LOCAL_CERT = cur.execute("select local_cert from vpn where id=(?);", (indx,)).fetchone()[0]
            DB_VPN_REMOTE_CERT = cur.execute("select remote_cert from vpn where id=(?);", (indx,)).fetchone()[0]
            if DB_VPN_IPSEC_EN == 0:
                DB_VPN_AUTO = 'ignore'
            elif DB_VPN_IPSEC_EN == 1 and DB_VPN_START_MODE == 1:
                DB_VPN_AUTO = 'start'
            elif DB_VPN_IPSEC_EN == 1 and DB_VPN_START_MODE == 0:
                DB_VPN_AUTO = 'add'
            else:
                pass

            VPN_IPSEC_CONF_RULES += 'conn {}\n'.format(DB_VPN_CONN_NAME)
            VPN_IPSEC_CONF_RULES += '        authby={}\n'.format(DB_VPN_AUTH_MODE)
            VPN_IPSEC_CONF_RULES += '        aggressive={}\n'.format(DB_VPN_OPER_MODE)
            VPN_IPSEC_CONF_RULES += '        keyexchange={}\n'.format(DB_VPN_IKE_MODE)
            VPN_IPSEC_CONF_RULES += '        dpdaction={}\n'.format(DB_VPN_DPD_ACTION)
            VPN_IPSEC_CONF_RULES += '        dpddelay={}\n'.format(DB_VPN_DPD_DELAY)
            VPN_IPSEC_CONF_RULES += '        dpdtimeout={}\n'.format(DB_VPN_DPD_TIMEOUT)
            VPN_IPSEC_CONF_RULES += '        ike={}\n'.format(DB_VPN_IKE_ENCRYPT)
            VPN_IPSEC_CONF_RULES += '        esp={}\n'.format(DB_VPN_ESP)
            VPN_IPSEC_CONF_RULES += '        lifetime={}\n'.format(DB_VPN_LIFETIME)
            VPN_IPSEC_CONF_RULES += '        rekey={}\n'.format(DB_VPN_REKEY)
            VPN_IPSEC_CONF_RULES += '        left=%any\n'
            if DB_VPN_AUTH_MODE == 'pubkey':
                VPN_IPSEC_CONF_RULES += '        leftcert=local/{}\n'.format(DB_VPN_LOCAL_CERT)
            VPN_IPSEC_CONF_RULES += '        leftsubnet={}\n'.format(DB_VPN_LEFT_SUBNET)
            VPN_IPSEC_CONF_RULES += '        leftid=\"{}\"\n'.format(DB_VPN_LEFTID)
            VPN_IPSEC_CONF_RULES += '        right={}\n'.format(DB_VPN_RIGHT)
            if DB_VPN_AUTH_MODE == 'pubkey':
                VPN_IPSEC_CONF_RULES += '        rightcert=remote/{}\n'.format(DB_VPN_REMOTE_CERT)
            VPN_IPSEC_CONF_RULES += '        rightsubnet={}\n'.format(DB_VPN_RIGHT_SUBNET)
            VPN_IPSEC_CONF_RULES += '        rightid=\"{}\"\n'.format(DB_VPN_RIGHTID)
            VPN_IPSEC_CONF_RULES += '        auto={}\n'.format(DB_VPN_AUTO)
            if DB_VPN_AUTH_MODE == 'pubkey':
                VPN_IPSEC_SECRETS_RULES += '\"{}\" : RSA {}\n'.format(DB_VPN_RIGHTID, DB_VPN_LOCAL_CERT)
            elif DB_VPN_AUTH_MODE == 'psk':
                VPN_IPSEC_SECRETS_RULES += '\"{}\" : PSK {}\n'.format(DB_VPN_RIGHTID, DB_VPN_PSK)
            else:
                pass

        # genVpnConf(VPN_IPSEC_CONF_RULES)
        # _cmd = '/usr/sbin/update-rc.d -f ipsec defaults'
        # os.system(_cmd)

    ''' SNMP agent setting '''
    ''''''

    ''' OpenVPN setting '''
    DB_OPENVPN_EN = cur.execute("select active from openvpn").fetchone()[0]
    if DB_OPENVPN_EN == 1:
        DB_OPENVPN_CONF = cur.execute("select conf from openvpn").fetchone()[0]

        if not os.path.exists(os.environ['SYS_OPENVPN_CONF_DIR']):
            _cmd = 'mkdir -p {}'.format(os.environ['SYS_OPENVPN_CONF_DIR'])
            os.system(_cmd)

        _cmd = 'rm -f {}/*'.format(os.environ['SYS_OPENVPN_CONF_DIR'])
        os.system(_cmd)
        _cmd = 'cp -f {}/{} {}'.format(os.environ['MLB_OPENVPN_CONF_DIR'],
                                       DB_OPENVPN_CONF,
                                       os.environ['SYS_OPENVPN_CONF_DIR'])
        os.system(_cmd)
        _cmd = '/usr/sbin/update-rc.d -f openvpn defaults'
        # os.system(_cmd)

    else:
        pass
        _cmd = '/usr/sbin/update-rc.d -f openvpn remove'
        # os.system(_cmd)

    con.close()

    ''' Generate iptables config file. '''
    _cmd = '/usr/bin/python gen-iptables-rules.py'
    # os.system(_cmd)


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/tmp/web_update_all.log',
                        format='%(asctime)s %(levelname)s: %(message)s')

    if not os.path.exists(os.environ['WEB_APP_DB_PATH']):
        log.error('Database not found, please check.')
        sys.exit(1)
    else:
        main()