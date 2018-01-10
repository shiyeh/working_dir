#!/usr/bin/python
# This script will generate a iptable according to
# its rules.

import os
import sys
import sqlite3
import init_env
import logging

log = logging.getLogger(__name__)


class genTable(object):
    """docstring for genTable"""
    def __init__(self):
        super(genTable, self).__init__()
        global IPTBL_FILTER_RULES
        global IPTBL_NAT_RULES
        global WEB_APP_DB_PATH

        IPTBL_FILTER_RULES = ""
        IPTBL_NAT_RULES = ""

    def portForwarding(self):
        global IPTBL_FILTER_RULES
        global IPTBL_NAT_RULES
        log.info('Generate ruels for portForwarding.')

        DB_NAT_PORTFW_PROTOCOL = ""
        DB_NAT_PORTFW_IP = ""
        DB_NAT_PORTFW_INTERNAL = ""
        DB_NAT_PORTFW_PUBLIC = ""

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()

        for indx in xrange(1, 32):
            DB_NAT_PORTFW_EN = cur.execute("select active from port_forwarding where id=(?);", (indx,)).fetchone()[0]
            log.debug('DB_NAT_PORTFW_EN = {}'.format(DB_NAT_PORTFW_EN))

            if DB_NAT_PORTFW_EN == 1:
                rule = 'select ip from port_forwarding where id=(?)'
                DB_NAT_PORTFW_IP = cur.execute(rule, (indx,)).fetchone()[0]
                rule = 'select public_port from port_forwarding where id=(?)'
                DB_NAT_PORTFW_PUBLIC = cur.execute(rule, (indx,)).fetchone()[0]
                PUBLIC_LIST = DB_NAT_PORTFW_PUBLIC.split('-')
                rule = 'select internal_port from port_forwarding where id=(?)'
                DB_NAT_PORTFW_INTERNAL = cur.execute(rule, (indx,)).fetchone()[0]
                INTERNAL_LIST = DB_NAT_PORTFW_INTERNAL.split('-')
                rule = 'select protocol from port_forwarding where id=(?)'
                DB_NAT_PORTFW_PROTOCOLS = cur.execute(rule, (indx,)).fetchone()[0]

                PROTOCOL_LIST = DB_NAT_PORTFW_PROTOCOLS.split('/')
                for DB_NAT_PORTFW_PROTOCOL in PROTOCOL_LIST:
                    if len(PUBLIC_LIST) == 2 or len(INTERNAL_LIST) == 2:
                        IPTBL_FILTER_RULES += "-A FORWARD -d {}/32 -p {} -m {} --dport {}:{} ".format(DB_NAT_PORTFW_IP,
                                                                                                   DB_NAT_PORTFW_PROTOCOL,
                                                                                                   DB_NAT_PORTFW_PROTOCOL,
                                                                                                   INTERNAL_LIST[0],
                                                                                                   INTERNAL_LIST[1])
                        IPTBL_FILTER_RULES += "-m state --state NEW,RELATED,ESTABLISHED -j ACCEPT"
                        IPTBL_FILTER_RULES += '\n'

                        IPTBL_NAT_RULES += "-A PREROUTING -i {} -p {} -m {} --dport {}:{} -j DNAT --to-destination {}:{}-{}".format(os.environ["MLB_IFACE"],
                                                                                                                              DB_NAT_PORTFW_PROTOCOL,
                                                                                                                              DB_NAT_PORTFW_PROTOCOL,
                                                                                                                              PUBLIC_LIST[0],
                                                                                                                              PUBLIC_LIST[1],
                                                                                                                              DB_NAT_PORTFW_IP,
                                                                                                                              INTERNAL_LIST[0],
                                                                                                                              INTERNAL_LIST[1])
                        IPTBL_NAT_RULES += '\n'
                    else:
                        IPTBL_FILTER_RULES += "-A FORWARD -d {}/32 -p {} -m {} --dport {} ".format(DB_NAT_PORTFW_IP,
                                                                                                   DB_NAT_PORTFW_PROTOCOL,
                                                                                                   DB_NAT_PORTFW_PROTOCOL,
                                                                                                   DB_NAT_PORTFW_INTERNAL)
                        IPTBL_FILTER_RULES += "-m state --state NEW,RELATED,ESTABLISHED -j ACCEPT"
                        IPTBL_FILTER_RULES += '\n'

                        IPTBL_NAT_RULES += "-A PREROUTING -i {} -p {} -m {} --dport {} -j DNAT --to-destination {}:{}".format(os.environ["MLB_IFACE"],
                                                                                                                              DB_NAT_PORTFW_PROTOCOL,
                                                                                                                              DB_NAT_PORTFW_PROTOCOL,
                                                                                                                              DB_NAT_PORTFW_PUBLIC,
                                                                                                                              DB_NAT_PORTFW_IP,
                                                                                                                              DB_NAT_PORTFW_INTERNAL)
                        IPTBL_NAT_RULES += '\n'
        con.close()

    def lanForwarding(self):
        global IPTBL_FILTER_RULES
        log.info('Generate ruels for lanForwarding.')

        IPTBL_FILTER_RULES += "-A FORWARD -i eth0 -o %s -j ACCEPT" % (os.environ["MLB_IFACE"])
        IPTBL_FILTER_RULES += '\n'

    def genIpsec(self):
        global IPTBL_NAT_RULES

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()
        DB_VPN_ACTIVE = cur.execute("select active from vpn_active").fetchone()[0]

        if DB_VPN_ACTIVE == 1:
            log.info('Generate ruels for IPSEC.')

            for indx in xrange(1, 6):
                DB_VPN_IPSEC_EN = cur.execute("select ipsec from vpn where id=(?);", (indx,)).fetchone()[0]
                if DB_VPN_IPSEC_EN == 1:
                    DB_VPN_LEFT_SUBNET = cur.execute("select leftsubnet from vpn where id=(?);", (indx,)).fetchone()[0]
                    IPTBL_NAT_RULES += "-A POSTROUTING -s %s -o %s -m policy --dir out --pol ipsec -j ACCEPT" % (DB_VPN_LEFT_SUBNET, os.environ["MLB_IFACE"])
                    IPTBL_NAT_RULES += '\n'
                    IPTBL_NAT_RULES += "-A POSTROUTING -s %s -o %s -j MASQUERADE" % (DB_VPN_LEFT_SUBNET, os.environ["MLB_IFACE"])
                    IPTBL_NAT_RULES += '\n'
        else:
            log.info('IPSEC Disabled.')

        con.close()

    def genOpenVPN(self):
        global IPTBL_NAT_RULES

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()

        DB_IF_ADDR_IP = cur.execute(
            "select ip_addr from lan_setting").fetchone()[0]

        # Calculate netmask to CIDR
        DB_IF_MASK_STR = cur.execute(
            "select submask from lan_setting").fetchone()[0]
        IF_CIDR = sum([bin(int(x)).count(
            "1") for x in DB_IF_MASK_STR.split(".")])

        DB_OPENVPN_EN = cur.execute("select active from openvpn").fetchone()[0]
        if DB_OPENVPN_EN == 1:
            log.info('Generate rules for OpenVPN.')
            IPTBL_NAT_RULES += "-A POSTROUTING -s %s/%s -o tun+ -j MASQUERADE" % (DB_IF_ADDR_IP, IF_CIDR)
            IPTBL_NAT_RULES += '\n'
        else:
            log.info('OpenVPN Disabled.')

        con.close()

    def doNormalNatRule(self):
        # Here is normal NAT rule.
        global IPTBL_NAT_RULES
        log.info('Generate normal rules for NAT.')

        IPTBL_NAT_RULES += "-A POSTROUTING -o %s -j MASQUERADE" % (os.environ["MLB_IFACE"])
        IPTBL_NAT_RULES += '\n'

    def blockHttp(self):
        global IPTBL_FILTER_RULES

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()
        WAN_AL_HTTP_EN = cur.execute("select wan_allow_http from service_setting where id=1").fetchone()[0]
        LAN_AL_HTTP_EN = cur.execute("select lan_allow_http from service_setting where id=1").fetchone()[0]
        con.close()

        # Here is for WAN
        if WAN_AL_HTTP_EN == 0:
            log.debug('WAN_AL_HTTP_EN is disabled.')
            TMP_ACT = "DROP"
        else:
            TMP_ACT = "ACCEPT"

        TMP_RULES = "-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 80 -m state --state NEW -j %s" % (TMP_ACT)
        IPTBL_FILTER_RULES += "-A INPUT -i {} {}".format(os.environ["MLB_IFACE"], TMP_RULES)
        IPTBL_FILTER_RULES += '\n'

        # Here is for LAN
        if LAN_AL_HTTP_EN == 0:
            TMP_ACT = "DROP"
            TMP_RULES = "-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 80 -m state --state NEW -j %s" % (TMP_ACT)
            IPTBL_FILTER_RULES += "-A INPUT -i eth0 %s" % (TMP_RULES)
            IPTBL_FILTER_RULES += '\n'
        else:
            log.debug('LAN_AL_HTTP_EN is enabled.')

    def blockHttps(self):
        global IPTBL_FILTER_RULES

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()
        WAN_AL_HTTPS_EN = cur.execute("select wan_allow_https from service_setting where id=1").fetchone()[0]
        LAN_AL_HTTPS_EN = cur.execute("select lan_allow_https from service_setting where id=1").fetchone()[0]
        con.close()

        # Here is for WAN
        if WAN_AL_HTTPS_EN == 0:
            log.debug('WAN_AL_HTTPS_EN is disabled.')
            TMP_ACT = "DROP"
        else:
            TMP_ACT = "ACCEPT"

        TMP_RULES = "-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 443 -m state --state NEW -j %s" % (TMP_ACT)
        IPTBL_FILTER_RULES += "-A INPUT -i %s %s" % (os.environ["MLB_IFACE"], TMP_RULES)
        IPTBL_FILTER_RULES += '\n'

        # Here is for LAN
        if LAN_AL_HTTPS_EN == 0:
            TMP_ACT = "DROP"
            TMP_RULES = "-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 443 -m state --state NEW -j %s" % (TMP_ACT)
            IPTBL_FILTER_RULES += "-A INPUT -i eth0 %s" % (TMP_RULES)
            IPTBL_FILTER_RULES += '\n'
        else:
            log.debug('LAN_AL_HTTPS_EN is enabled.')

    def blockSsh(self):
        global IPTBL_FILTER_RULES

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()
        WAN_AL_SSH_EN = cur.execute("select wan_allow_ssh from service_setting where id=1").fetchone()[0]
        LAN_AL_SSH_EN = cur.execute("select lan_allow_ssh from service_setting where id=1").fetchone()[0]
        con.close()

        # Here is for WAN
        if WAN_AL_SSH_EN == 0:
            TMP_ACT = "DROP"
        else:
            log.debug('WAN_AL_SSH_EN is enabled.')
            TMP_ACT = "ACCEPT"

        TMP_RULES = "-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 22 -m state --state NEW -j %s" % (TMP_ACT)
        IPTBL_FILTER_RULES += "-A INPUT -i %s %s" % (os.environ["MLB_IFACE"], TMP_RULES)
        IPTBL_FILTER_RULES += '\n'

        # Here is for LAN
        if LAN_AL_SSH_EN == 0:
            TMP_ACT = "DROP"
            TMP_RULES = "-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 22 -m state --state NEW -j %s" % (TMP_ACT)
            IPTBL_FILTER_RULES += "-A INPUT -i eth0 %s" % (TMP_RULES)
            IPTBL_FILTER_RULES += '\n'
        else:
            log.debug('LAN_AL_SSH_EN is enabled.')

    def blockPing(self):
        global IPTBL_FILTER_RULES

        con = sqlite3.connect(os.environ['WEB_APP_DB_PATH'])
        cur = con.cursor()
        DB_AL_PING_EN = cur.execute("select allow_ping from lan_setting where id=1").fetchone()[0]
        con.close()

        # Block icmp packet from WAN, it's also default value.
        if DB_AL_PING_EN == 0:
            TMP_RULES = "-p icmp --icmp-type 8 -s 0/0 -d 0/0 -m state --state NEW -j DROP"
            IPTBL_FILTER_RULES += "-A INPUT -i %s %s" % (os.environ["MLB_IFACE"], TMP_RULES)
            IPTBL_FILTER_RULES += '\n'
        else:
            log.debug('DB_AL_PING_EN is enabled.')


def genIptableConf():
    try:
        # Generate /opt/mlis/conf/iptables.ppp0.ipv4.nat file or
        #          /opt/mlis/conf/iptables.wwan1.ipv4.nat
        with open(os.environ['MLB_PPP_NAT_PATH'], 'w+') as f:
            tmp = '# Begin ' + os.environ["MLB_PPP_NAT_PATH"] + '\n'
            tmp += '*filter\n'
            tmp += ':INPUT ACCEPT [0:0]\n'
            tmp += ':FORWARD ACCEPT [0:0]\n'
            tmp += ':OUTPUT ACCEPT [0:0]\n'
            tmp += IPTBL_FILTER_RULES
            tmp += 'COMMIT\n'
            tmp += '*nat\n'
            tmp += ':PREROUTING ACCEPT [0:0]\n'
            tmp += ':INPUT ACCEPT [0:0]\n'
            tmp += ':OUTPUT ACCEPT [0:0]\n'
            tmp += ':POSTROUTING ACCEPT [0:0]\n'
            tmp += IPTBL_NAT_RULES
            tmp += 'COMMIT\n'
            tmp += '# End ' + os.environ["MLB_PPP_NAT_PATH"] + '\n'

            f.write(tmp)

    except Exception as e:
        log.exception(e)
    else:
        log.info('Generate configuration file successfully.')
        log.info('Check if %s is exists.', os.environ['MLB_PPP_NAT_PATH'])
    finally:
        f.close()


def runGenRule():
    ''' Store these function as the following order in list,
        and call them later. '''
    t = genTable()
    ruleLists = [t.portForwarding, t.lanForwarding, t.genIpsec,
                 t.genOpenVPN, t.doNormalNatRule, t.blockHttp,
                 t.blockHttps, t.blockSsh, t.blockPing]

    log.info('*** Start to generate rules for {}. ***'.format(os.environ["MLB_IFACE"]))
    # Now call them via for loop
    for f in ruleLists:
        try:
            f()
        except Exception as e:
            log.exception(e)
            sys.exit(1)

    log.info('All iptable rules have been generated.')


def main():
    os.environ["MLB_IFACE"] = ""

    ''' Do runGenRule() while MLB_IFACE = wwan1 and ppp0 '''
    for os.environ["MLB_IFACE"] in ["wwan1", "ppp0"]:
        if os.environ["MLB_IFACE"] == "wwan1":
            tmp = ""
            tmp += os.environ["MLB_CONF_DIR"]
            tmp += '/'
            tmp += os.environ["MLB_WWAN_NAT_CFG"]
            os.environ["MLB_PPP_NAT_PATH"] = tmp
            runGenRule()
        elif os.environ["MLB_IFACE"] == "ppp0":
            tmp = ""
            tmp += os.environ["MLB_CONF_DIR"]
            tmp += '/'
            tmp += os.environ["MLB_PPP_NAT_CFG"]
            os.environ["MLB_PPP_NAT_PATH"] = tmp
            runGenRule()
        else:
            log.debug('MLB_IFACE not found.')

        # When iptable rules generate, write it down to a configuration file.
        genIptableConf()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/tmp/iptableRule.log',
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
