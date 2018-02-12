#!/bin/sh

if [ -f "${MLB_BAK_DIR}" ]
    then
        set -x
        cp "${MLB_BAK_DIR}/ipsec.d.old" "${SYS_VPN_CONF_DIR}"


        chmod 664 "${SYS_NETWORK_DIR}/${MLB_NETWORK_IFACES}"
        chmod 664 "${SYS_DIR}/${MLB_DHCP_CFG}"

        ####### generate udhcpd config file
        ### source gen-dhcpd-conf.sh
        update-rc.d udhcpd defaults
        update-rc.d -f busybox-udhcpd remove
        update-rc.d -f ntpd remove

        chmod +x "${SYS_PPP_DIR}/${MLB_PPP_ON_BOOT}"
        update-rc.d ppp defaults

        chmod +x "${PPP_SETNAT_PATH}"
        chmod +x "${PPP_UPDATEWEB_PATH}"
        chmod +x "${WWAN_UPDATEWEN_PATH}"

        update-rc.d web-console defaults
        update-rc.d ipsec defaults

        chmod 664 "${WEB_APP_DB_PATH}"
        chmod 664 "${WEB_STAT_DB_PATH}"

        source /opt/mlis/web-update-all.sh
        ####### generate udhcpd config file
        source /opt/mlis/gen-init-G420x-conf.sh
        chmod +x "${MLB_INIT_PATH}"

        chmod +x "${MLB_CONF_BIN}/serial-config"
        chmod +x "${MLB_CONF_BIN}/serial-socket"

        set +x
