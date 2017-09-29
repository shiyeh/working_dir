#!/usr/bin/python
import os
import socket
import fcntl
import struct


def get_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])


def get_ip_addr_sub(ifname):
    tmp = get_ip_addr(ifname).split('.')
    return '{}.{}.{}'.format(tmp[0], tmp[1], tmp[2])


def get_netmask(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x891b,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])


if os.path.exists('/opt/mlis/'):
    # System directory list
    os.environ["SYS_DIR"] = "/etc"
    os.environ["SYS_PPP_DIR"] = "/etc/ppp"
    os.environ["SYS_PPP_PEERS_DIR"] = "/etc/ppp/peers"
    os.environ["SYS_NETWORK_DIR"] = "/etc/network"
    os.environ["SYS_NGINX_DIR"] = "/etc/nginx"
    os.environ["SYS_OPENVPN_CONF_DIR"] = os.environ["SYS_DIR"] + "/openvpn"
    os.environ["SYS_VPN_CONF_DIR"] = os.environ["SYS_DIR"] + "/ipsec.d"
    os.environ["SYS_STRONGSWAN_CONF_DIR"] = os.environ["SYS_DIR"] + "/strongswan.d"
    os.environ["SYS_VPN_CAS_DIR"] = os.environ["SYS_VPN_CONF_DIR"] + "/cacerts"
    os.environ["SYS_VPN_CERTS_DIR"] = os.environ["SYS_VPN_CONF_DIR"] + "/certs"
    os.environ["SYS_VPN_CERTS_LOCAL_DIR"] = os.environ["SYS_VPN_CONF_DIR"] + "/certs/local"
    os.environ["SYS_VPN_CERTS_REMOTE_DIR"] = os.environ["SYS_VPN_CONF_DIR"] + "/certs/remote"
    os.environ["SYS_VPN_PRIVATE_KEY_DIR"] = os.environ["SYS_VPN_CONF_DIR"] + "/private"
    os.environ["SYS_SNMP_CFG_DIR"] = os.environ["SYS_DIR"] + "/snmp"
    os.environ["SYS_LOGROTATE_CFG_DIR"] = os.environ["SYS_DIR"] + "/logrotate.d"

    # System config file list (full path)
    os.environ["SYS_DEF_UDHCPD"] = os.environ["SYS_DIR"] + "/init.d/udhcpd"
    os.environ["SYS_BB_UDHCPD"] = os.environ["SYS_DIR"] + "/init.d/busybox-udhcpd"
    os.environ["SYS_NGINX_WEBCON_EN"] = os.environ["SYS_DIR"] + "/init.d/web-console"
    os.environ["SYS_SNMP_EN"] = os.environ["SYS_DIR"] + "/init.d/snmpd"
    os.environ["SYS_NGINX_CFG"] = os.environ["SYS_NGINX_DIR"] + "/nginx.conf"
    os.environ["SYS_NGINX_SITE_EN_CFG"] = os.environ["SYS_NGINX_DIR"] + "/sites-enabled/web_console"
    os.environ["SYS_NGINX_MIME_TYPE"] = os.environ["SYS_NGINX_DIR"] + "/mime.types"
    os.environ["SYS_VPN_CFG"] = os.environ["SYS_DIR"] + "/ipsec.conf"
    os.environ["SYS_VPN_SECRETS"] = os.environ["SYS_DIR"] + "/ipsec.secrets"
    os.environ["SYS_VPN_STRONGSWAN_CFG"] = os.environ["SYS_DIR"] + "/strongswan.conf"
    os.environ["SYS_IPSEC_PATH"] = os.environ["SYS_DIR"] + "/init.d/ipsec"
    os.environ["SYS_SNMP_CFG_PATH"] = "/etc/snmp/snmpd.conf"
    os.environ["SYS_STRONGSWAN_JUNK_PATH"] = os.environ["SYS_STRONGSWAN_CONF_DIR"] + "/pkcs11_plugin.conf"
    os.environ["SYS_VPN_ROOT_CA_PATH"] = os.environ["SYS_VPN_CAS_DIR"] + "/caCert.der"
    os.environ["SYS_VPN_ROOT_CA_KEY_PATH"] = os.environ["SYS_VPN_PRIVATE_KEY_DIR"] + "/caKey.der"

    # MLB config directory
    os.environ["MLB_DIR"] = "/opt/mlis"
    os.environ["MLB_CONF_DIR"] = os.environ["MLB_DIR"] + "/conf"
    os.environ["MLB_CONF_BIN"] = os.environ["MLB_DIR"] + "/bin"
    os.environ["MLB_WEBCON_DIR"] = os.environ["MLB_DIR"] + "/web_console"
    os.environ["MLB_MDM_DIR"] = os.environ["MLB_DIR"] + "/mdm_management"
    os.environ["MLB_WEBCON_APP_DIR"] = os.environ["MLB_WEBCON_DIR"] + "/app"
    os.environ["MLB_OPENVPN_CONF_DIR"] = os.environ["MLB_CONF_DIR"] + "/openvpn"

    # MLB config file name
    os.environ["MLB_INIT"] = "init-G420x"
    os.environ["MLB_INIT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_INIT"]
    os.environ["MLB_DHCP_CFG"] = "udhcpd.conf"
    os.environ["MLB_NETWORK_IFACES"] = "interfaces"
    os.environ["MLB_PPP_ON_BOOT"] = "ppp_on_boot"
    os.environ["MLB_PPP_APN_OPT"] = "apn_opt"
    os.environ["MLB_QMI_APN_OPT"] = "qmi-network.conf"
    os.environ["MLB_PPP_PEER"] = "cdma"
    os.environ["MLB_PPP_PEER_CHAT"] = "cdma_chat"
    os.environ["MLB_PPP_SET_NAT"] = "50setnat"
    os.environ["MLB_PPP_UPDATE_WEB"] = "90updateWeb"
    os.environ["MLB_PPP_NAT_CFG"] = "iptables.ppp0.ipv4.nat"
    os.environ["MLB_WWAN_NAT_CFG"] = "iptables.wwan1.ipv4.nat"
    os.environ["MLB_WWAN_UPDATE_WEB"] = "90wwanupdateWeb"

    # MLB config file list (full path)
    os.environ["MLB_NETWORK_IFECES_PATH"] = os.environ["MLB_DIR"] + '/' + os.environ["MLB_NETWORK_IFACES"]
    os.environ["MLB_DHCP_CFG_PATH"] = os.environ["MLB_DIR"] + '/' + os.environ["MLB_DHCP_CFG"]
    os.environ["MLB_PPP_ON_BOOT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_ON_BOOT"]
    os.environ["MLB_PPP_APN_OPT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_APN_OPT"]
    os.environ["MLB_QMI_APN_OPT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_QMI_APN_OPT"]
    os.environ["MLB_PPP_PEER_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_PEER"]
    os.environ["MLB_PPP_PEER_CHAT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_PEER_CHAT"]
    os.environ["MLB_PPP_NAT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_NAT_CFG"]
    os.environ["MLB_PPP_SET_NAT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_SET_NAT"]
    os.environ["MLB_PPP_UPDATEWEB_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_PPP_UPDATE_WEB"]
    os.environ["MLB_WWAN_UPDATE_WEB_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_WWAN_UPDATE_WEB"]
    os.environ["MLB_WWAN_NAT_PATH"] = os.environ["MLB_CONF_DIR"] + '/' + os.environ["MLB_WWAN_NAT_CFG"]
    os.environ["MLB_NGINX_WEBCON_EN"] = os.environ["MLB_CONF_DIR"] + "/web-console"
    os.environ["MLB_SNMP_EN"] = os.environ["MLB_CONF_DIR"] + "/snmpd"
    os.environ["MLB_SNMP_CFG_PATH"] = os.environ["MLB_CONF_DIR"] + "/snmpd.conf"
    os.environ["MLB_NGINX_CFG_PATH"] = os.environ["MLB_CONF_DIR"] + "/nginx.conf"
    os.environ["MLB_NGINX_SITE_EN_CFG_PATH"] = os.environ["MLB_CONF_DIR"] + "/web_console"
    os.environ["MLB_NGINX_MIME_TYPE_PATH"] = os.environ["MLB_CONF_DIR"] + "/mime.types"
    os.environ["MLB_VPN_CFG_PATH"] = os.environ["MLB_CONF_DIR"] + "/ipsec.conf"
    os.environ["MLB_VPN_SECRETS_PATH"] = os.environ["MLB_CONF_DIR"] + "/ipsec.secrets"
    os.environ["MLB_VPN_STRONGSWAN_CFG_PATH"] = os.environ["MLB_CONF_DIR"] + "/strongswan.conf"

    # System variables
    os.environ["DHCPD_USED_IF"] = "ens33"
    os.environ["WEB_APP_DB_PATH"] = "/opt/mlis/web_console/app/app.db"
    os.environ["WEB_APP_DBTMP_PATH"] = "/tmp/app.db"
    os.environ["WEB_APP_DBBAK_PATH"] = os.environ["MLB_CONF_DIR"] + "/app.db.bak"
    os.environ["WEB_STAT_DB_PATH"] = os.environ["MLB_WEBCON_DIR"] + "/app/status.db"
    os.environ["WEB_STAT_DBBAK_PATH"] = os.environ["MLB_CONF_DIR"] + "/status.db.bak"
    os.environ["PPP_SETNAT_PATH"] = os.environ["SYS_PPP_DIR"] + '/ip-up.d' + os.environ["MLB_PPP_SET_NAT"]
    os.environ["PPP_UPDATEWEB_PATH"] = os.environ["SYS_PPP_DIR"] + '/ip-up.d' + os.environ["MLB_PPP_UPDATE_WEB"]
    os.environ["WWAN_UPDATEWEN_PATH"] = os.environ["SYS_NETWORK_DIR"] + '/if-up.d' + os.environ["MLB_WWAN_UPDATE_WEB"]
    os.environ["IF_ADDR_IP"] = get_ip_addr(os.environ["DHCPD_USED_IF"])
    os.environ["IF_MASK_STR"] = get_netmask(os.environ["DHCPD_USED_IF"])
    os.environ["IF_ADDR_SUB"] = get_ip_addr_sub(os.environ["DHCPD_USED_IF"])
    os.environ["DHCPD_IP_RANG_BGN"] = os.environ["IF_ADDR_SUB"] + '.20'
    os.environ["DHCPD_IP_RANG_END"] = os.environ["IF_ADDR_SUB"] + '.22'


print os.environ["IF_ADDR_IP"]
print os.environ["IF_MASK_STR"]
print os.environ["IF_ADDR_SUB"]
print os.environ["DHCPD_IP_RANG_BGN"]
print os.environ["DHCPD_IP_RANG_END"]
