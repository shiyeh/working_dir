#!/usr/bin/python

import os
import init_mlb_env


def main():
    print 'DHCPD_IP_RANG_BGN = ', os.environ["DHCPD_IP_RANG_BGN"]
    print 'DHCPD_IP_RANG_END = ', os.environ["DHCPD_IP_RANG_END"]
    print 'IF_MASK_STR = ', os.environ["IF_MASK_STR"]

    print os.environ["MLB_CONF_DIR"] + "/" + os.environ["MLB_PPP_NAT_CFG"]
    # print os.environ['MLB_PPP_NAT_PATH']

    print '[WARNING] Now the interface is %s' % os.environ["DHCPD_USED_IF"]
    print os.environ['MLB_PPP_NAT_PATH']


if __name__ == '__main__':
    main()
