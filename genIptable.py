#!/usr/bin/python
import init_env
import os, sys


class genTable(object):
    """docstring for genTable"""
    def __init__(self):
        super(genTable, self).__init__()
        global IPTBL_FILTER_RULES
        global IPTBL_NAT_RULES
        global WEB_APP_DB_PATH

        IPTBL_FILTER_RULES = ""
        IPTBL_NAT_RULES = ""

    def lanForwarding(self):
        global IPTBL_FILTER_RULES
        # log.info('Generate ruels for lanForwarding.')

        IPTBL_FILTER_RULES += "-A FORWARD -i eth0 -o %s -j ACCEPT" % ('test')
        IPTBL_FILTER_RULES += '\n'

        return IPTBL_FILTER_RULES


def runGenRule(MLB_IFACE):
    ''' Store these function as the following order in list,
        and call them later. '''
    # t = genTable()
    # ruleLists = [t.portForwarding, t.lanForwarding, t.genIpsec,
    #              t.genOpenVPN, t.doNormalNatRule, t.blockHttp,
    #              t.blockHttps, t.blockSsh, t.blockPing]

    # log.info('*** Start to generate rules for {}. ***'.format(MLB_IFACE))
    # Now call them via for loop
    # for f in ruleLists:
    #     try:
    #         f()
    #     except Exception as e:
    #         log.exception(e)
    #         sys.exit(1)

    print('Now is runGenRule on {}'.format(MLB_IFACE))

    # log.info('All iptable rules have been generated.')


def main():
    MLB_IFACE = ""

    ''' Do runGenRule() while MLB_IFACE = wwan1 and ppp0 '''
    for MLB_IFACE in ["wwan1", "ppp0"]:
        if MLB_IFACE == "wwan1":
            tmp = ""
            tmp += os.environ["MLB_CONF_DIR"]
            tmp += '/'
            tmp += os.environ["MLB_WWAN_NAT_CFG"]
            os.environ["MLB_PPP_NAT_PATH"] = tmp
            # runGenRule(MLB_IFACE)
        elif MLB_IFACE == "ppp0":
            tmp = ""
            tmp += os.environ["MLB_CONF_DIR"]
            tmp += '/'
            tmp += os.environ["MLB_PPP_NAT_CFG"]
            os.environ["MLB_PPP_NAT_PATH"] = tmp
            # runGenRule(MLB_IFACE)
        else:
            # log.debug('MLB_IFACE not found.')
            pass

    genTable().lanForwarding()
    print(IPTBL_FILTER_RULES)


if __name__ == '__main__':
    main()
