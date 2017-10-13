#!/usr/bin/python

import os
import sys
import sqlite3
import init_mlb_env
import logging

log = logging.getLogger(__name__)


def genVpnConf(VPN_IPSEC_CONF_RULES):
    # _vpnConfPath = os.environ['MLB_VPN_CFG_PATH']
    _vpnConfPath = '/tmp/vpn_conf'

    # Generate /opt/mlis/conf/ipsec.conf file
    with open(_vpnConfPath, 'w+') as f:
        _tmp = '#!/bin/sh\n'
        _tmp += '# Begin ' + _vpnConfPath + '\n'
        _tmp += '# ipsec.conf - strongSwan IPsec configuration file\n'
        _tmp += '\n'
        _tmp += '# basic configuration\n'
        _tmp += '\n'
        _tmp += 'config setup\n'
        _tmp += '        # strictcrlpolicy=yes\n'
        _tmp += '        # uniqueids = no\n'
        _tmp += '\n'
        _tmp += '# Add connections here.\n'
        _tmp += '\n'
        _tmp += 'conn %default\n'
        _tmp += '        mobike=no\n'
        _tmp += '        keyingtries=%forever\n'
        _tmp += '\n'
        _tmp += VPN_IPSEC_CONF_RULES
        _tmp += '# End {}\n'.format(_vpnConfPath)

        f.write(_tmp)


def genSnmpConf():
    pass


def genApnConf(PRISIM, BCKINGSIM, DB_APN, DB_USR_NAME, DB_PASS_WRD,
               DB_2ND_APN, DB_2ND_USR_NAME, DB_2ND_PASS_WRD):
    # _apnConfPath = os.environ['MLB_PPP_APN_OPT_PATH']
    _apnConfPath = '/tmp/apn_opt'

    # Generate /opt/mlis/conf/apn_opt file
    try:
        with open(_apnConfPath, 'w+') as f:
            _tmp = '#!/bin/sh\n'
            _tmp += '# Begin ' + _apnConfPath + '\n'
            _tmp += 'export MLBPRISIM=\"' + 'sim{}\"\n'.format(PRISIM)
            _tmp += 'export MLBBCKSIM=\"' + 'sim{}\"\n'.format(BCKINGSIM)
            _tmp += '\n'
            _tmp += 'export MLBAPN1={}\n'.format(DB_APN)
            _tmp += 'export MLBPDPYTPE1=ip\n'
            _tmp += 'export MLBUSRNAME1={}\n'.format(DB_USR_NAME)
            _tmp += 'export MLBPASSWORD1={}\n'.format(DB_PASS_WRD)
            _tmp += 'export MLBAPN2={}\n'.format(DB_2ND_APN)
            _tmp += 'export MLBPDPYTPE2=ip\n'
            _tmp += 'export MLBUSRNAME2={}\n'.format(DB_2ND_USR_NAME)
            _tmp += 'export MLBPASSWORD2={}\n'.format(DB_2ND_PASS_WRD)
            _tmp += '\n'
            _tmp += '# End {}\n'.format(_apnConfPath)

            f.write(_tmp)
    except Exception as e:
        log.exception(e)
    else:
        return 0
    finally:
        f.close()


def genDhcpdConf(DHCPD_IP_START, DHCPD_IP_END, DHCP_STATIC_LEASE,
                 DB_DHCP_IP_DNS, DB_DHCP_IP_SEC_DNS, DHCP_IP_SUBMASK,
                 IF_ADDR_IP, DHCP_CLIENT_TIME):
    # _dhcpdConfPath = os.environ['SYS_DIR'] + '/' + os.environ['MLB_DHCP_CFG']
    _dhcpdConfPath = '/tmp/dhcpdConfPath'

    # Generate /etc/udhcpd.conf file
    try:
        with open(_dhcpdConfPath, 'w+') as f:
            _tmp = '# Begin {}\n'.format(_dhcpdConfPath)
            _tmp += '# The start and end of the IP lease block\n'
            _tmp += 'start       {}\n'.format(DHCPD_IP_START)
            _tmp += 'end         {}\n'.format(DHCPD_IP_END)
            _tmp += '# The interface that udhcpd will use\n'
            _tmp += 'interface {}\n'.format(os.environ['DHCPD_USED_IF'])
            _tmp += '# The location of the pid file\n'
            _tmp += 'pidfile     /var/run/udhcpd.pid\n\n'
            _tmp += '# Static leases map\n'
            _tmp += '{}\n\n'.format(DHCP_STATIC_LEASE)
            _tmp += '''# The remainder of options are DHCP options and can be specified with the
# keyword 'opt' or 'option'. If an option can take multiple items, such
# as the dns option, they can be listed on the same line, or multiple
# lines.\n'''
            _tmp += 'opt         dns     {} {} #public google dns servers\n'.format(DB_DHCP_IP_DNS, DB_DHCP_IP_SEC_DNS)
            _tmp += 'option      subnet  {}\n'.format(DHCP_IP_SUBMASK)
            _tmp += 'opt         router  {}\n'.format(IF_ADDR_IP)
            _tmp += 'option      lease   {} # default: 10 days\n'.format(DHCP_CLIENT_TIME)
            _tmp += '# Arbitrary option in hex form:\n'
            _tmp += 'option      0x08    01020304 # option 8: "cookie server IP addr: 1.2.3.4"\n'
            _tmp += '# The location of the leases file\n'
            _tmp += 'lease_file     /var/lib/misc/udhcpd.leases\n\n'
            _tmp += '# End {}\n'.format(_dhcpdConfPath)

            f.write(_tmp)
    except Exception as e:
        log.exception(e)
    else:
        return 0
    finally:
        f.close()


def genNetIfConf(IF_ADDR_IP, IF_MASK_STR,
                 IF_NETWORK, IF_BROADCAST):
    # _netIfPath = os.environ['SYS_NETWORK_DIR'] + '/' + os.environ['MLB_NETWORK_IFACES']
    _netIfPath = '/tmp/pawwwwwthhhh'
    # print _netIfPath

    # Generate /etc/network/interfaces file
    try:
        with open(_netIfPath, 'w+') as f:
            _tmp = '# Begin ' + _netIfPath + '\n'
            _tmp += '# The loopback interface\n'
            _tmp += 'auto lo\n'
            _tmp += 'iface lo inet loopback\n'
            _tmp += '\n# Wired interfaces\n'
            _tmp += 'auto eth0\n'
            _tmp += 'iface eth0 inet static\n'
            _tmp += '    address     {}\n'.format(IF_ADDR_IP)
            _tmp += '    netmask     {}\n'.format(IF_MASK_STR)
            _tmp += '    network     {}\n'.format(IF_NETWORK)
            _tmp += '    broadcast   {}\n'.format(IF_BROADCAST)
            _tmp += '\niface wwan1 inet dhcp\n'
            _tmp += '# End {}\n'.format(_netIfPath)

            f.write(_tmp)
    except Exception as e:
        log.error(e)
    else:
        return 0
    finally:
        f.close()


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

    if genNetIfConf(IF_ADDR_IP, IF_MASK_STR,
                    IF_NETWORK, IF_BROADCAST) != 0:
        log.debug('genNetIfConf() generate failed !')

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

    if genDhcpdConf(DHCPD_IP_START, DHCPD_IP_END, DHCP_STATIC_LEASE,
                    DB_DHCP_IP_DNS, DB_DHCP_IP_SEC_DNS, DHCP_IP_SUBMASK,
                    IF_ADDR_IP, DHCP_CLIENT_TIME) != 0:
        log.debug('genDhcpdConf() generate failed !')

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

    if genApnConf(PRISIM, BCKINGSIM, DB_APN, DB_USR_NAME, DB_PASS_WRD,
                  DB_2ND_APN, DB_2ND_USR_NAME, DB_2ND_PASS_WRD) != 0:
        log.debug('genApnConf() generate failed !')

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
    DB_SNMP_EN = cur.execute("select active from snmp_agent").fetchone()[0]
    if DB_SNMP_EN == 1:
        DB_SNMP_AC = ''
        ref = 0

        DB_SNMP_READ_COMMUNITY = cur.execute("select read_community from snmp_agent").fetchone()[0]
        DB_SNMP_WRITE_COMMUNITY = cur.execute("select write_community from snmp_agent").fetchone()[0]
        DB_SNMP_AGENT_VER = cur.execute("select agent_ver from snmp_agent").fetchone()[0]
        if DB_SNMP_AGENT_VER > 1:
            ref += 4
        else:
            ref += 0

        DB_SNMP_AUTH_PROTO = cur.execute("select auth_protocol from snmp_agent").fetchone()[0]
        if DB_SNMP_AUTH_PROTO > 0:
            ref += 2
        else:
            ref += 0
        if DB_SNMP_AUTH_PROTO == 0:
            DB_SNMP_AUTH_PROTO = ''
        if DB_SNMP_AUTH_PROTO == 1:
            DB_SNMP_AUTH_PROTO = 'MD5'
        if DB_SNMP_AUTH_PROTO == 2:
            DB_SNMP_AUTH_PROTO = 'SHA'

        DB_SNMP_AUTH_KEY = cur.execute("select auth_key from snmp_agent").fetchone()[0]
        DB_SNMP_PRIV_PROTO = cur.execute("select priv_protocol from snmp_agent").fetchone()[0]
        if DB_SNMP_PRIV_PROTO > 0:
            ref += 1
        else:
            ref += 0
        if DB_SNMP_PRIV_PROTO == 0:
            DB_SNMP_PRIV_PROTO = ''
        if DB_SNMP_PRIV_PROTO == 1:
            DB_SNMP_PRIV_PROTO = 'DES'
        if DB_SNMP_PRIV_PROTO == 2:
            DB_SNMP_PRIV_PROTO = 'AES'

        if not os.path.exists(os.environ['SYS_SNMP_CFG_DIR']):
            _cmd = 'mkdir -p {}'.format(os.environ['SYS_SNMP_CFG_DIR'])
            os.system(_cmd)

        genSnmpConf()

        os.system(_cmd)
        _cmd = '/usr/sbin/update-rc.d -f snmpd defaults'
        # os.system(_cmd)
    else:
        _cmd = '/usr/sbin/update-rc.d -f snmpd remove'
        # os.system(_cmd)

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
