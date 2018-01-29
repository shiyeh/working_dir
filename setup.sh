#!/bin/sh
source /opt/mlis/init-mlb-env.sh

if [ -f ${MLB_INIT_PATH} ]
then
	source "${MLB_INIT_PATH}"
	echo "mlb_init: ${mlb_init}"

	if [ -d "/opt/log" ]
	then
		echo "LOG output directory: /opt/log existed."
	else
		echo "Created LOG output directory."
		mkdir "/opt/log"
	fi
	exit 1
else
	if [ -f "${MLB_DIR}/pkg/setup.sh" ]
	then
		chmod +x "${MLB_DIR}/pkg/setup.sh"
		/bin/sh "${MLB_DIR}/pkg/setup.sh"
		rm -f "${MLB_DIR}/pkg/setup.sh"
		echo "Installed IPK."
		sync
		sync
		sync
		reboot
		exit 1
	fi

	if [ -d "${MLB_CONF_DIR}" ]
	then
        chmod +x ${MLB_DIR}/*.sh
		chmod +x ${MLB_DIR}/*.py
	fi

	####### backup "/etc/network/interfaces"
	if [ -f "${SYS_NETWORK_DIR}/${MLB_NETWORK_IFACES}" ]
	then
		set -x
		mv -f "${SYS_NETWORK_DIR}/${MLB_NETWORK_IFACES}" "${SYS_NETWORK_DIR}/${MLB_NETWORK_IFACES}.bak"
		cp -f "${MLB_NETWORK_IFECES_PATH}" "${SYS_NETWORK_DIR}/${MLB_NETWORK_IFACES}"
		chmod 664 "${SYS_NETWORK_DIR}/${MLB_NETWORK_IFACES}"
		set +x
	fi

	####### generate network interface config file
	#### source gen-netif-conf.sh


	### Brad's Workaround, copy busybox-udhcpd to replace udhcpd,
	if [ -f "${SYS_BB_UDHCPD}" ]
	then
		cp -f "${SYS_BB_UDHCPD}" "${SYS_DEF_UDHCPD}"
	fi

	####### backup "/etc/udhcpd.conf"
	if [ -f "${SYS_DIR}/${MLB_DHCP_CFG}" ]
	then
		set -x
		mv -f "${SYS_DIR}/${MLB_DHCP_CFG}" "${SYS_DIR}/${MLB_DHCP_CFG}.bak"
		set +x
	fi
	cp -f "${MLB_CONF_DIR}/${MLB_DHCP_CFG}" "${SYS_DIR}/${MLB_DHCP_CFG}"
	chmod 664 "${SYS_DIR}/${MLB_DHCP_CFG}"

	####### generate udhcpd config file
	### source gen-dhcpd-conf.sh
	update-rc.d udhcpd defaults
	update-rc.d -f busybox-udhcpd remove
	update-rc.d -f ntpd remove

	if [ -f "${MLB_PPP_PEER_PATH}" ] && [ -f "${MLB_PPP_PEER_CHAT_PATH}" ]
	then
		cp -f "${MLB_PPP_PEER_PATH}" "${SYS_PPP_PEERS_DIR}/."
		cp -f "${MLB_PPP_PEER_CHAT_PATH}" "${SYS_PPP_PEERS_DIR}/."

		if [ -f "${MLB_PPP_ON_BOOT_PATH}" ]
		then
			cp -f "${MLB_PPP_ON_BOOT_PATH}" "${SYS_PPP_DIR}/."
			chmod +x "${SYS_PPP_DIR}/${MLB_PPP_ON_BOOT}"
			update-rc.d ppp defaults
		fi
	fi

	set -x

	if [ -f "${MLB_PPP_NAT_PATH}" ]
	then
		cp -f "${MLB_PPP_NAT_PATH}" "${SYS_DIR}/."

		if [ -e "${MLB_PPP_SET_NAT_PATH}" ]
		then
			cp -f "${MLB_PPP_SET_NAT_PATH}" "${PPP_SETNAT_PATH}"
			chmod +x "${PPP_SETNAT_PATH}"
		fi
		if [ -e "${MLB_PPP_UPDATEWEB_PATH}" ]
		then
			cp -f "${MLB_PPP_UPDATEWEB_PATH}" "${PPP_UPDATEWEB_PATH}"
			chmod +x "${PPP_UPDATEWEB_PATH}"
		fi
	fi

	if [ -f "${MLB_WWAN_NAT_PATH}" ]
	then
		cp -f "${MLB_WWAN_NAT_PATH}" "${SYS_DIR}/."

		if [ -f "${MLB_WWAN_UPDATE_WEB_PATH}" ]
		then
			cp -f "${MLB_WWAN_UPDATE_WEB_PATH}" "${WWAN_UPDATEWEN_PATH}"
			chmod +x "${WWAN_UPDATEWEN_PATH}"
		fi
	fi

	if [ -f "${MLB_NGINX_CFG_PATH}" ]
	then
		cp -f "${MLB_NGINX_CFG_PATH}" "${SYS_NGINX_CFG}"
	fi

	if [ -f "${MLB_NGINX_SITE_EN_CFG_PATH}" ]
	then
		cp -f "${MLB_NGINX_SITE_EN_CFG_PATH}" "${SYS_NGINX_SITE_EN_CFG}"
	fi

	if [ -f "${MLB_NGINX_MIME_TYPE_PATH}" ]
	then
		cp -f "${MLB_NGINX_MIME_TYPE_PATH}" "${SYS_NGINX_MIME_TYPE}"
	fi

	if [ -f "${MLB_NGINX_WEBCON_EN}" ]
	then
		cp -f "${MLB_NGINX_WEBCON_EN}" "${SYS_NGINX_WEBCON_EN}"
		update-rc.d web-console defaults
	fi

	####### generate ipsec config file

    if [ -f "${MLB_VPN_STRONGSWAN_CFG_PATH}" ]
    then
        cp -f "${MLB_VPN_STRONGSWAN_CFG_PATH}" "${SYS_VPN_STRONGSWAN_CFG}"
    fi

    if [ ! -f "${SYS_IPSEC_PATH}" ]
    then
        SYS_IPSEC_COMM_PATH=`which ipsec`
        ln -s "${SYS_IPSEC_COMM_PATH}" "${SYS_IPSEC_PATH}"
        update-rc.d ipsec defaults
    fi

    if  [ -f "${SYS_STRONGSWAN_JUNK_PATH}" ]
    then
        rm -rf ${SYS_STRONGSWAN_JUNK_PATH}
    fi

    ####### generate ipsec certs dir default
    if [ ! -d "${SYS_VPN_CERTS_LOCAL_DIR}" ]
    then
        mkdir -p ${SYS_VPN_CERTS_LOCAL_DIR}
    fi

    if [ ! -d "${SYS_VPN_CERTS_REMOTE_DIR}" ]
    then
        mkdir -p ${SYS_VPN_CERTS_REMOTE_DIR}
    fi

    ####### generate app.db default
    if [ -f "${WEB_APP_DBBAK_PATH}" ]
    then
        cp -f "${WEB_APP_DBBAK_PATH}" "${WEB_APP_DB_PATH}"
    fi
    chmod 664 "${WEB_APP_DB_PATH}"

    ####### generate status.db default
    if [ -f "${WEB_STAT_DBBAK_PATH}" ]
    then
        cp -f "${WEB_STAT_DBBAK_PATH}" "${WEB_STAT_DB_PATH}"
    fi
    chmod 664 "${WEB_STAT_DB_PATH}"

	####### generate snmpd file
    if [ -f "${MLB_SNMP_EN}" ]
    then
        cp -f "${MLB_SNMP_EN}" "${SYS_SNMP_EN}"
    fi

    source /opt/mlis/web-update-all.sh
	####### generate udhcpd config file
	source /opt/mlis/gen-init-G420x-conf.sh
	chmod +x "${MLB_INIT_PATH}"

	chmod +x "${MLB_CONF_BIN}/serial-config"
	chmod +x "${MLB_CONF_BIN}/serial-socket"
	set +x

    ### Remove telnet service
    if [ -f /etc/init.d/telnetd ]
    then
	update-rc.d -f telnetd remove
    fi

    ### For timezone, make sure timezone change to default (UTC)
    cp -f /usr/share/zoneinfo/UTC /etc/localtime
fi

