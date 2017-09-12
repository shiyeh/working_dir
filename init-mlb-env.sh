#!/bin/sh

if [ -z ${MLB_DIR+x} ]
then
	echo "exporting MLB variables."
    ### System directory list
    export SYS_DIR="/etc"
    export SYS_PPP_DIR="/etc/ppp"
    export SYS_PPP_PEERS_DIR="/etc/ppp/peers"
    export SYS_NETWORK_DIR="/etc/network"
    export SYS_NGINX_DIR="/etc/nginx"
    export SYS_OPENVPN_CONF_DIR="${SYS_DIR}/openvpn"
    export SYS_VPN_CONF_DIR="${SYS_DIR}/ipsec.d"
    export SYS_STRONGSWAN_CONF_DIR="${SYS_DIR}/strongswan.d"
    export SYS_VPN_CAS_DIR="${SYS_VPN_CONF_DIR}/cacerts"
    export SYS_VPN_CERTS_DIR="${SYS_VPN_CONF_DIR}/certs"
    export SYS_VPN_CERTS_LOCAL_DIR="${SYS_VPN_CERTS_DIR}/local"
    export SYS_VPN_CERTS_REMOTE_DIR="${SYS_VPN_CERTS_DIR}/remote"
    export SYS_VPN_PRIVATE_KEY_DIR="${SYS_VPN_CONF_DIR}/private"
    export SYS_SNMP_CFG_DIR="${SYS_DIR}/snmp"
    export SYS_LOGROTATE_CFG_DIR="{SYS}/logrotate.d"

    ### System config file list (full path)
    export SYS_DEF_UDHCPD="${SYS_DIR}/init.d/udhcpd"
    export SYS_BB_UDHCPD="${SYS_DIR}/init.d/busybox-udhcpd"
    export SYS_NGINX_WEBCON_EN="${SYS_DIR}/init.d/web-console"
    export SYS_SNMP_EN="${SYS_DIR}/init.d/snmpd"
    export SYS_NGINX_CFG="${SYS_NGINX_DIR}/nginx.conf"
    export SYS_NGINX_SITE_EN_CFG="${SYS_NGINX_DIR}/sites-enabled/web_console"
    export SYS_NGINX_MIME_TYPE="${SYS_NGINX_DIR}/mime.types"
    export SYS_VPN_CFG="${SYS_DIR}/ipsec.conf"
    export SYS_VPN_SECRETS="${SYS_DIR}/ipsec.secrets" 
    export SYS_VPN_STRONGSWAN_CFG="${SYS_DIR}/strongswan.conf"
    export SYS_IPSEC_PATH="${SYS_DIR}/init.d/ipsec"
    export SYS_SNMP_CFG_PATH="${SYS_SNMP_CFG_DIR}/snmpd.conf"
    export SYS_STRONGSWAN_JUNK_PATH="${SYS_STRONGSWAN_CONF_DIR}/pkcs11_plugin.conf"
    export SYS_VPN_ROOT_CA_PATH="${SYS_VPN_CAS_DIR}/caCert.der"
    export SYS_VPN_ROOT_CA_KEY_PATH="${SYS_VPN_PRIVATE_KEY_DIR}/caKey.der"

    ### MLB config directory
    export MLB_DIR="/opt/mlis"
    export MLB_CONF_DIR="${MLB_DIR}/conf"
    export MLB_CONF_BIN="${MLB_DIR}/bin"
    export MLB_WEBCON_DIR="${MLB_DIR}/web_console"
    export MLB_MDM_DIR="${MLB_DIR}/mdm_management"
    export MLB_WEBCON_APP_DIR="${MLB_WEBCON_DIR}/app"
    export MLB_OPENVPN_CONF_DIR="${MLB_CONF_DIR}/openvpn"

    ### MLB config file name
    export MLB_INIT="init-G420x"
    export MLB_INIT_PATH="${MLB_CONF_DIR}/${MLB_INIT}"
    export MLB_DHCP_CFG="udhcpd.conf"
    export MLB_NETWORK_IFACES="interfaces"
    export MLB_PPP_ON_BOOT="ppp_on_boot"
    export MLB_PPP_APN_OPT="apn_opt"
    export MLB_QMI_APN_OPT="qmi-network.conf"
    export MLB_PPP_PEER="cdma"
    export MLB_PPP_PEER_CHAT="cdma_chat"
    export MLB_PPP_SET_NAT="50setnat"
    export MLB_PPP_UPDATE_WEB="90updateWeb"
    export MLB_PPP_NAT_CFG="iptables.ppp0.ipv4.nat"
    export MLB_WWAN_NAT_CFG="iptables.wwan1.ipv4.nat"
    export MLB_WWAN_UPDATE_WEB="90wwanupdateWeb"

    ### MLB config file list (full path)
    export MLB_NETWORK_IFECES_PATH="${MLB_CONF_DIR}/${MLB_NETWORK_IFACES}"
    export MLB_DHCP_CFG_PATH="${MLB_CONF_DIR}/${MLB_DHCP_CFG}"
    export MLB_PPP_ON_BOOT_PATH="${MLB_CONF_DIR}/${MLB_PPP_ON_BOOT}"
    export MLB_PPP_APN_OPT_PATH="${MLB_CONF_DIR}/${MLB_PPP_APN_OPT}"
    export MLB_QMI_APN_OPT_PATH="${MLB_CONF_DIR}/${MLB_QMI_APN_OPT}"
    export MLB_PPP_PEER_PATH="${MLB_CONF_DIR}/${MLB_PPP_PEER}"
    export MLB_PPP_PEER_CHAT_PATH="${MLB_CONF_DIR}/${MLB_PPP_PEER_CHAT}"
    export MLB_PPP_NAT_PATH="${MLB_CONF_DIR}/${MLB_PPP_NAT_CFG}"
    export MLB_PPP_SET_NAT_PATH="${MLB_CONF_DIR}/${MLB_PPP_SET_NAT}"
    export MLB_PPP_UPDATEWEB_PATH="${MLB_CONF_DIR}/${MLB_PPP_UPDATE_WEB}"
    export MLB_WWAN_UPDATE_WEB_PATH="${MLB_CONF_DIR}/${MLB_WWAN_UPDATE_WEB}"
    export MLB_WWAN_NAT_PATH="${MLB_CONF_DIR}/${MLB_WWAN_NAT_CFG}"
    export MLB_NGINX_WEBCON_EN="${MLB_CONF_DIR}/web-console"
    export MLB_SNMP_EN="${MLB_CONF_DIR}/snmpd"
    export MLB_SNMP_CFG_PATH="${MLB_CONF_DIR}/snmpd.conf"
    export MLB_NGINX_CFG_PATH="${MLB_CONF_DIR}/nginx.conf"
    export MLB_NGINX_SITE_EN_CFG_PATH="${MLB_CONF_DIR}/web_console"
    export MLB_NGINX_MIME_TYPE_PATH="${MLB_CONF_DIR}/mime.types"
    export MLB_VPN_CFG_PATH="${MLB_CONF_DIR}/ipsec.conf"
    export MLB_VPN_SECRETS_PATH="${MLB_CONF_DIR}/ipsec.secrets"
    export MLB_VPN_STRONGSWAN_CFG_PATH="${MLB_CONF_DIR}/strongswan.conf"

    ### System variables
    export DHCPD_USED_IF="ens33"
    export IF_ADDR_IP=`/sbin/ifconfig ${DHCPD_USED_IF} | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
    export IF_MASK_STR=`/sbin/ifconfig ${DHCPD_USED_IF} | grep 'inet addr:' | cut -d: -f4 | awk '{ print $1}'`
    export IF_ADDR_SUB=`echo ${IF_ADDR_IP} | awk -F. '{printf ("%s.%s.%s", $1, $2, $3)}'`
    export DHCPD_IP_RANG_BGN="${IF_ADDR_SUB}.20"
    export DHCPD_IP_RANG_END="${IF_ADDR_SUB}.22"
    export WEB_APP_DB_PATH="${MLB_WEBCON_DIR}/app/app.db"
    export WEB_APP_DBTMP_PATH="/tmp/app.db"
    export WEB_APP_DBBAK_PATH="${MLB_CONF_DIR}/app.db.bak"
    export WEB_STAT_DB_PATH="${MLB_WEBCON_DIR}/app/status.db"
    export WEB_STAT_DBBAK_PATH="${MLB_CONF_DIR}/status.db.bak"
    export PPP_SETNAT_PATH="${SYS_PPP_DIR}/ip-up.d/${MLB_PPP_SET_NAT}"
    export PPP_UPDATEWEB_PATH="${SYS_PPP_DIR}/ip-up.d/${MLB_PPP_UPDATE_WEB}"
    export WWAN_UPDATEWEN_PATH="${SYS_NETWORK_DIR}/if-up.d/${MLB_WWAN_UPDATE_WEB}"

    echo "Append ${MLB_DIR} to PATH."
    PATH=${MLB_DIR}:${PATH}
fi

