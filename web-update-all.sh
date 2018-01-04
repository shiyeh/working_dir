#!/bin/sh

source /opt/mlis/init-mlb-env.sh

if [ -f "${WEB_APP_DB_PATH}" ]; then
    ### calculate mask to cidr
    mask2cidr() {
        nbits=0
        IFS=.
        for dec in $1 ; do
            case $dec in
                255) let nbits+=8;;
                254) let nbits+=7;;
                252) let nbits+=6;;
                248) let nbits+=5;;
                240) let nbits+=4;;
                224) let nbits+=3;;
                192) let nbits+=2;;
                128) let nbits+=1;;
                0);;
                *);;
            esac
        done
        echo "$nbits"
    }
	### NETWORK INTERFACE configuration.
	DB_IF_ADDR_IP=`sqlite3 "${WEB_APP_DB_PATH}" 'select ip_addr from lan_setting'`
	DB_IF_MASK_STR=`sqlite3 "${WEB_APP_DB_PATH}" 'select submask from lan_setting'`

    IF_CIDR=$(mask2cidr ${DB_IF_MASK_STR})

	if [ "${DB_IF_ADDR_IP}" = "127.0.0.1" ]
	then
		echo "Err: Not allow IP setting, ${DB_IF_ADDR_IP}."
		exit 1
	fi

	IF_ADDR_SUB=`echo ${DB_IF_ADDR_IP} | awk -F. '{printf ("%s.%s.%s", $1, $2, $3)}'`
	IF_ADDR_IP="${DB_IF_ADDR_IP}"
	IF_MASK_STR="${DB_IF_MASK_STR}"
	source "${MLB_DIR}/gen-netif-conf.sh"

	### DHCP SEVER configuration.
	DB_DHCP_EN=`sqlite3 "${WEB_APP_DB_PATH}" 'select dhcp_server from dhcp_server'`
	DHCPD_IP_RANG_BGN=`sqlite3 "${WEB_APP_DB_PATH}" 'select start_ip from dhcp_server'`
	IPADDRSUB=`echo ${DHCPD_IP_RANG_BGN} | awk -F. '{printf ("%s.%s.%s", $1, $2, $3)}'`
	DB_DHCP_IP_SUBMSK=`sqlite3 "${WEB_APP_DB_PATH}" 'select submask from dhcp_server'`
	DB_DHCP_IP_DNS=`sqlite3 "${WEB_APP_DB_PATH}" 'select dns from dhcp_server'`
	DB_DHCP_IP_SEC_DNS=`sqlite3 "${WEB_APP_DB_PATH}" 'select sec_dns from dhcp_server'`
	DB_DHCP_IP_START=`echo ${DHCPD_IP_RANG_BGN} | cut -d. -f4 | awk '{ print $1}'`
	DB_DHCP_IP_NUM=`sqlite3 "${WEB_APP_DB_PATH}" 'select max_users from dhcp_server'`
	DB_DHCP_IP_END=$(($DB_DHCP_IP_START+$DB_DHCP_IP_NUM-1))
    DB_DHCP_IP_CLIENT_TIME=`sqlite3 "${WEB_APP_DB_PATH}" 'select client_time from dhcp_server'`

	DHCPD_IP_RANG_BGN="${IPADDRSUB}.${DB_DHCP_IP_START}"
	DHCPD_IP_RANG_END="${IPADDRSUB}.${DB_DHCP_IP_END}"
	DHCP_IP_GW=`sqlite3 "${WEB_APP_DB_PATH}" 'select gateway from dhcp_server'`
	DHCP_IP_SUBMASK="${DB_DHCP_IP_SUBMSK}"

	export DHCP_STATIC_LEASE=""
	for indx in {1..5}
	do
		rule="select active from dhcp_mapping where id=${indx}"
		DB_DHCP_STATIC_EN=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
		if [ "${DB_DHCP_STATIC_EN}" = 1 ]
		then
			rule="select ip from dhcp_mapping where id=${indx}"
			DB_DHCP_STC_IP=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
			rule="select mac from dhcp_mapping where id=${indx}"
			DB_DHCP_STC_MAC=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`

			# Static leases map
			#static_lease 00:60:08:11:CE:4E 192.168.0.54
			#static_lease 00:60:08:11:CE:3E 192.168.0.44
			DHCP_STATIC_LEASE+="static_lease ${DB_DHCP_STC_MAC} ${DB_DHCP_STC_IP}"
			DHCP_STATIC_LEASE+=$'\n'
		fi
	done
    if [ "${DB_DHCP_EN}" = 1 ]
    then
        /usr/sbin/update-rc.d -f udhcpd defaults
    else
        /usr/sbin/update-rc.d -f udhcpd remove
    fi
	source "${MLB_DIR}/gen-dhcpd-conf.sh"

	### MODEM INTERNET CONNECTION setting.
    PRISIM=`sqlite3 "${WEB_APP_DB_PATH}" "select priority from wan_priority_setting where id=1"`
    if [ ${PRISIM} == "1" ]
    then
        BCKINGSIM="2"
    elif [ ${PRISIM} == "2" ]
    then
        BCKINGSIM="1"
    else
        PRISIM="1"
        BCKINGSIM="2"
    fi

    export DB_APN=`sqlite3 "${WEB_APP_DB_PATH}" "select apn from wan_setting where id=1"`
    export DB_USR_NAME=`sqlite3 "${WEB_APP_DB_PATH}" "select username from wan_setting where id=1"`
    export DB_PASS_WRD=`sqlite3 "${WEB_APP_DB_PATH}" "select password from wan_setting where id=1"`
    export DB_2ND_APN=`sqlite3 "${WEB_APP_DB_PATH}" "select apn from wan_setting where id=2"`
    export DB_2ND_USR_NAME=`sqlite3 "${WEB_APP_DB_PATH}" "select username from wan_setting where id=2"`
    export DB_2ND_PASS_WRD=`sqlite3 "${WEB_APP_DB_PATH}" "select password from wan_setting where id=2"`

    source "${MLB_DIR}/gen-apn-conf.sh"
    echo "APN=${DB_APN}" > "${MLB_QMI_APN_OPT_PATH}"
    if [ -n "${DB_USR_NAME}" ] && [ -n "${DB_PASS_WRD}" ]
    then
        echo "${DB_USR_NAME}    *    ${DB_PASS_WRD}" > "${MLB_CONF_DIR}/pap-secrets"
    else
        echo "" > "${MLB_CONF_DIR}/pap-secrets"
    fi

    ###===========VPN Setting==========================
    DB_VPN_ACTIVE=`sqlite3 "${WEB_APP_DB_PATH}" "select active from vpn_active"`
    echo DB_VPN_ACTIVE = ${DB_VPN_ACTIVE}
    DB_VPN_POSTROUTING_INDX=()
    export VPN_IPSEC_CONF_RULES=""
    export VPN_IPSEC_SECRETS_RULES=""
    if [ "${DB_VPN_ACTIVE}" = 0 ]; then
        /usr/sbin/update-rc.d -f ipsec remove
    else
        for indx in {1..5}
        do
            rule="select active from vpn where id=${indx}"
            rule="select ipsec from vpn where id=${indx}"
            DB_VPN_IPSEC_EN=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            if [ "${DB_VPN_IPSEC_EN}" = 0 ]; then
                continue
            fi
            DB_VPN_POSTROUTING_INDX+=(${indx})
            rule="select conn_name from vpn where id=${indx}"
            DB_VPN_CONN_NAME=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select _left from vpn where id=${indx}"
            DB_VPN_LEFT=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select startup_mode from vpn where id=${indx}"
            DB_VPN_START_MODE=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select leftsubnet from vpn where id=${indx}"
            DB_VPN_LEFT_SUBNET=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select leftid from vpn where id=${indx}"
            DB_VPN_LEFTID=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select _right from vpn where id=${indx}"
            DB_VPN_RIGHT=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select rightsubnet from vpn where id=${indx}"
            DB_VPN_RIGHT_SUBNET=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select rightid from vpn where id=${indx}"
            DB_VPN_RIGHTID=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select keyexchange from vpn where id=${indx}"
            DB_VPN_IKE_MODE=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select aggressive from vpn where id=${indx}"
            DB_VPN_OPER_MODE=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select ike from vpn where id=${indx}"
            DB_VPN_IKE_ENCRYPT=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select lifetime from vpn where id=${indx}"
            DB_VPN_LIFETIME=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select rekey from vpn where id=${indx}"
            DB_VPN_REKEY=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select esp from vpn where id=${indx}"
            DB_VPN_ESP=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select dpdaction from vpn where id=${indx}"
            DB_VPN_DPD_ACTION=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select dpddelay from vpn where id=${indx}"
            DB_VPN_DPD_DELAY=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select dpdtimeout from vpn where id=${indx}"
            DB_VPN_DPD_TIMEOUT=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select auth_mode from vpn where id=${indx}"
            DB_VPN_AUTH_MODE=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select psk from vpn where id=${indx}"
            DB_VPN_PSK=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select local_cert from vpn where id=${indx}"
            DB_VPN_LOCAL_CERT=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            rule="select remote_cert from vpn where id=${indx}"
            DB_VPN_REMOTE_CERT=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
            if [ "${DB_VPN_IPSEC_EN}" = 0 ]; then
                DB_VPN_AUTO="ignore"
            elif [ "${DB_VPN_IPSEC_EN}" = 1 -a "${DB_VPN_START_MODE}" = 1 ]; then
                DB_VPN_AUTO="start"
            elif [ "${DB_VPN_IPSEC_EN}" = 1 -a "${DB_VPN_START_MODE}" = 0 ]; then
                DB_VPN_AUTO="add"
            fi

            VPN_IPSEC_CONF_RULES+="conn ${DB_VPN_CONN_NAME}"$'\n'
            VPN_IPSEC_CONF_RULES+="        authby=${DB_VPN_AUTH_MODE}"$'\n'
            VPN_IPSEC_CONF_RULES+="        aggressive=${DB_VPN_OPER_MODE}"$'\n'
            VPN_IPSEC_CONF_RULES+="        keyexchange=${DB_VPN_IKE_MODE}"$'\n'
            VPN_IPSEC_CONF_RULES+="        dpdaction=${DB_VPN_DPD_ACTION}"$'\n'
            VPN_IPSEC_CONF_RULES+="        dpddelay=${DB_VPN_DPD_DELAY}"$'\n'
            VPN_IPSEC_CONF_RULES+="        dpdtimeout=${DB_VPN_DPD_TIMEOUT}"$'\n'
            VPN_IPSEC_CONF_RULES+="        ike=${DB_VPN_IKE_ENCRYPT}"$'\n'
            VPN_IPSEC_CONF_RULES+="        esp=${DB_VPN_ESP}"$'\n'
            VPN_IPSEC_CONF_RULES+="        lifetime=${DB_VPN_LIFETIME}"$'\n'
            VPN_IPSEC_CONF_RULES+="        rekey=${DB_VPN_REKEY}"$'\n'
            VPN_IPSEC_CONF_RULES+="        left=%any"$'\n'
            if [ "${DB_VPN_AUTH_MODE}" = "pubkey" ]; then
                VPN_IPSEC_CONF_RULES+="        leftcert=local/${DB_VPN_LOCAL_CERT}"$'\n'
            fi
            VPN_IPSEC_CONF_RULES+="        leftsubnet=${DB_VPN_LEFT_SUBNET}"$'\n'
            VPN_IPSEC_CONF_RULES+="        leftid=\"${DB_VPN_LEFTID}\""$'\n'
            VPN_IPSEC_CONF_RULES+="        right=${DB_VPN_RIGHT}"$'\n'
            if [ "${DB_VPN_AUTH_MODE}" = "pubkey" ]; then
                VPN_IPSEC_CONF_RULES+="        rightcert=remote/${DB_VPN_REMOTE_CERT}"$'\n'
            fi
            VPN_IPSEC_CONF_RULES+="        rightsubnet=${DB_VPN_RIGHT_SUBNET}"$'\n'
            VPN_IPSEC_CONF_RULES+="        rightid=\"${DB_VPN_RIGHTID}\""$'\n'
            VPN_IPSEC_CONF_RULES+="        auto=${DB_VPN_AUTO}"$'\n'

            if [ "${DB_VPN_AUTH_MODE}" = "pubkey" ]; then
                VPN_IPSEC_SECRETS_RULES="\"${DB_VPN_RIGHTID}\" : RSA ${DB_VPN_LOCAL_CERT}"$'\n'
            elif [ "${DB_VPN_AUTH_MODE}" = "psk" ]; then
                VPN_IPSEC_SECRETS_RULES="\"${DB_VPN_RIGHTID}\" : PSK ${DB_VPN_PSK}"$'\n'
            fi
        done
        source gen-vpn-conf.sh
        /usr/sbin/update-rc.d -f ipsec defaults
    fi
    ###========snmp agent setting=================
    DB_SNMP_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select active from snmp_agent"`
    if [ "${DB_SNMP_EN}" = 1 ]
    then
        export DB_SNMP_AC=""
        ref=0
        DB_SNMP_READ_COMMUNITY=`sqlite3 "${WEB_APP_DB_PATH}" "select read_community from snmp_agent"`
        DB_SNMP_WRITE_COMMUNITY=`sqlite3 "${WEB_APP_DB_PATH}" "select write_community from snmp_agent"`
        DB_SNMP_AGENT_VER=`sqlite3 "${WEB_APP_DB_PATH}" "select agent_ver from snmp_agent"`
        if [ "${DB_SNMP_AGENT_VER}" -gt 1 ]; then let ref+=4 ; else let ref+=0 ; fi

        DB_SNMP_AUTH_PROTO=`sqlite3 "${WEB_APP_DB_PATH}" "select auth_protocol from snmp_agent"`
        if [ "${DB_SNMP_AUTH_PROTO}" -gt 0 ]; then let ref+=2 ; else let ref+=0 ; fi
        case ${DB_SNMP_AUTH_PROTO} in
            0) DB_SNMP_AUTH_PROTO='';;
            1) DB_SNMP_AUTH_PROTO="MD5";;
            2) DB_SNMP_AUTH_PROTO="SHA";;
        esac
        DB_SNMP_AUTH_KEY=`sqlite3 "${WEB_APP_DB_PATH}" "select auth_key from snmp_agent"`

        DB_SNMP_PRIV_PROTO=`sqlite3 "${WEB_APP_DB_PATH}" "select priv_protocol from snmp_agent"`
        if [ "${DB_SNMP_PRIV_PROTO}" -gt 0 ]; then let ref+=1 ; else let ref+=0 ; fi
        case ${DB_SNMP_PRIV_PROTO} in
            0) DB_SNMP_PRIV_PROTO='';;
            1) DB_SNMP_PRIV_PROTO="DES";;
            2) DB_SNMP_PRIV_PROTO="AES";;
        esac
        DB_SNMP_PRIV_KEY=`sqlite3 "${WEB_APP_DB_PATH}" "select priv_key from snmp_agent"`

        if [ ${ref} -ge 4 ]; then DB_SNMP_AC+="createUser ${DB_SNMP_READ_COMMUNITY}" ; fi
        if [ ${ref} -ge 6 ]; then DB_SNMP_AC+=" ${DB_SNMP_AUTH_PROTO} \"${DB_SNMP_AUTH_KEY}\"" ; fi
        if [ ${ref} -ge 7 ]; then DB_SNMP_AC+=" ${DB_SNMP_PRIV_PROTO} \"${DB_SNMP_PRIV_KEY}\"" ; fi

        DB_SNMP_AC+=$'\n'
        DB_SNMP_AC+=$'\n'
        if [ ${DB_SNMP_AGENT_VER} -le 2 ];
        then
            DB_SNMP_AC+="#        sec.name  source          community"$'\n'
            DB_SNMP_AC+="com2sec  readonly  default         ${DB_SNMP_READ_COMMUNITY}"$'\n'
            DB_SNMP_AC+="com2sec  readwrite default         ${DB_SNMP_WRITE_COMMUNITY}"$'\n'
            DB_SNMP_AC+=$'\n'
        fi
        DB_SNMP_AC+="#             sec.model  sec.name"$'\n'
        DB_SNMP_AC+="group RWGroup v1         readwrite"$'\n'
        DB_SNMP_AC+="group RWGroup v2c        readwrite"$'\n'
        DB_SNMP_AC+="group RWGroup usm        ${DB_SNMP_READ_COMMUNITY}"$'\n'
        DB_SNMP_AC+="group ROGroup v1         readonly"$'\n'
        DB_SNMP_AC+="group ROGroup v2c        readonly"$'\n'
        DB_SNMP_AC+="group ROGroup usm        ${DB_SNMP_READ_COMMUNITY}"$'\n'

        if [ ! -d ${SYS_SNMP_CFG_DIR} ];
        then
            mkdir -p ${SYS_SNMP_CFG_DIR}
        fi
        source gen-snmp-conf.sh
        /usr/sbin/update-rc.d -f snmpd defaults
    else
        /usr/sbin/update-rc.d -f snmpd remove
    fi

    ###========OpenVPN setting=================
    DB_OPENVPN_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select active from openvpn"`
    if [ "${DB_OPENVPN_EN}" = 1 ]
    then
        DB_OPENVPN_CONF=`sqlite3 "${WEB_APP_DB_PATH}" "select conf from openvpn"`

        if [ ! -d "${SYS_OPENVPN_CONF_DIR}" ]
        then
            mkdir -p ${SYS_OPENVPN_CONF_DIR}
        fi

        rm -f ${SYS_OPENVPN_CONF_DIR}/*
        cp -f ${MLB_OPENVPN_CONF_DIR}/${DB_OPENVPN_CONF} ${SYS_OPENVPN_CONF_DIR}
        /usr/sbin/update-rc.d -f openvpn defaults
    else
        /usr/sbin/update-rc.d -f openvpn remove
    fi

    ### Here is start to generate iptables rules. There are 2 config files.
    ### 1) iptables.ppp0.ipv4.nat
    ### 2) iptables.wwan1.ipv4.nat

    export MLB_IFACE=(ppp0 wwan1)

    for MLB_IFACE in ${MLB_IFACE[@]}; do
    	export IPTBL_FILTER_RULES=""
    	export IPTBL_NAT_RULES=""

    	BACKUP_PATH="${MLB_PPP_NAT_PATH}"

    	if [ "${MLB_IFACE}" == "wwan1" ]; then
            MLB_PPP_NAT_PATH="${MLB_CONF_DIR}/${MLB_WWAN_NAT_CFG}"
        elif [ "${MLB_IFACE}" == "ppp0" ]; then
            MLB_PPP_NAT_PATH="${MLB_CONF_DIR}/${MLB_PPP_NAT_CFG}"
        else
            echo "MLB_IFACE not found."
            echo "Exit."
            exit 1
        fi

        # block/allow new http connection from Public IP/WWAN interface.
        WAN_AL_HTTP_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select wan_allow_http from service_setting where id=1"`
        if [ "${WAN_AL_HTTP_EN}" = 0 ]
        then
            TMP_ACT="DROP"
        else
            TMP_ACT="ACCEPT"
        fi
        TMP_RULES="-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 80 -m state --state NEW -j ${TMP_ACT}"
        IPTBL_FILTER_RULES+="-A INPUT -i ${MLB_IFACE} ${TMP_RULES}"
        IPTBL_FILTER_RULES+=$'\n'

        # block/allow new https connection from Public IP/WWAN interface.
        WAN_AL_HTTPS_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select wan_allow_https from service_setting where id=1"`
        if [ "${WAN_AL_HTTPS_EN}" = 0 ]
        then
            TMP_ACT="DROP"
        else
            TMP_ACT="ACCEPT"
        fi
        TMP_RULES="-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 443 -m state --state NEW -j ${TMP_ACT}"
        IPTBL_FILTER_RULES+="-A INPUT -i ${MLB_IFACE} ${TMP_RULES}"
        IPTBL_FILTER_RULES+=$'\n'

        # block/allow new ssh connection from Public IP/WWAN interface.
        WAN_AL_SSH_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select wan_allow_ssh from service_setting where id=1"`
        if [ "${WAN_AL_SSH_EN}" = 0 ]
        then
            TMP_ACT="DROP"
        else
            TMP_ACT="ACCEPT"
        fi
        TMP_RULES="-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 22 -m state --state NEW -j ${TMP_ACT}"
        IPTBL_FILTER_RULES+="-A INPUT -i ${MLB_IFACE} ${TMP_RULES}"
        IPTBL_FILTER_RULES+=$'\n'

        # blocking new icmp connection from Public IP/WWAN interface if users not allow.
        DB_AL_PING_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select allow_ping from lan_setting where id=1"`
        # Default value is not allowed.
        if [ "${DB_AL_PING_EN}" = 0 ]
        then
            TMP_RULES="-p icmp --icmp-type 8 -s 0/0 -d 0/0 -m state --state NEW -j DROP"
            IPTBL_FILTER_RULES+="-A INPUT -i ${MLB_IFACE} ${TMP_RULES}"
            IPTBL_FILTER_RULES+=$'\n'
        fi

        ### Port Forwarding setting.
    	for indx in {1..32}
    	do
    		rule="select active from port_forwarding where id=${indx}"
    		DB_NAT_PORTFW_EN=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
    		if [ "${DB_NAT_PORTFW_EN}" = 1 ]
    		then
    			rule="select ip from port_forwarding where id=${indx}"
                DB_NAT_PORTFW_IP=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`

                rule="select public_port from port_forwarding where id=${indx}"
                DB_NAT_PORTFW_PUBLIC=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
                rule="select internal_port from port_forwarding where id=${indx}"
                DB_NAT_PORTFW_INTERNAL=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
                OIFS="$IFS"
                IFS="-"
                read -a PUBLIC_TMP <<< "${DB_NAT_PORTFW_PUBLIC}"
                read -a INTERNAL_TMP <<< "${DB_NAT_PORTFW_INTERNAL}"
                IFS="$OIFS"

                if [ "${#PUBLIC_TMP[@]}" = 2 ]; then
                    DB_NAT_PORTFW_PUBLIC="${PUBLIC_TMP[0]}:${PUBLIC_TMP[1]}"
                fi
                if [ "${#INTERNAL_TMP[@]}" = 2 ]; then
                    DB_NAT_PORTFW_INTERNAL="${INTERNAL_TMP[0]}-${INTERNAL_TMP[1]}"
                fi

                rule="select protocol from port_forwarding where id=${indx}"
                DB_NAT_PORTFW_PROTOCOLS=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`

                OIFS="$IFS"
                IFS="/"
                for DB_NAT_PORTFW_PROTOCOL in $DB_NAT_PORTFW_PROTOCOLS; do
                    IPTBL_FILTER_RULES+="-A FORWARD -d ${DB_NAT_PORTFW_IP}/32 -p ${DB_NAT_PORTFW_PROTOCOL} -m ${DB_NAT_PORTFW_PROTOCOL} --dport ${DB_NAT_PORTFW_PUBLIC} -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT"
                    IPTBL_FILTER_RULES+=$'\n'
                    IPTBL_NAT_RULES+="-A PREROUTING -i ${MLB_IFACE} -p ${DB_NAT_PORTFW_PROTOCOL} -m ${DB_NAT_PORTFW_PROTOCOL} --dport ${DB_NAT_PORTFW_PUBLIC} -j DNAT --to-destination ${DB_NAT_PORTFW_IP}:${DB_NAT_PORTFW_INTERNAL}"
                    IPTBL_NAT_RULES+=$'\n'
                done
                IFS="$OIFS"
    		fi
    	done

        ###=============== For LAN iptables settings ===============
        LAN_AL_HTTP_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select lan_allow_http from service_setting where id=1"`
        if [ "${LAN_AL_HTTP_EN}" = 0 ]
        then
            TMP_ACT="DROP"
            TMP_RULES="-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 80 -m state --state NEW -j ${TMP_ACT}"
            IPTBL_FILTER_RULES+="-A INPUT -i eth0 ${TMP_RULES}"
            IPTBL_FILTER_RULES+=$'\n'
        else
            echo "Enable LAN_AL_HTTP!"
        fi

        LAN_AL_HTTPS_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select lan_allow_https from service_setting where id=1"`
        if [ "${LAN_AL_HTTPS_EN}" = 0 ]
        then
            TMP_ACT="DROP"
            TMP_RULES="-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 443 -m state --state NEW -j ${TMP_ACT}"
            IPTBL_FILTER_RULES+="-A INPUT -i ${MLB_IFACE} ${TMP_RULES}"
            IPTBL_FILTER_RULES+=$'\n'
        else
            echo "Enable LAN_AL_HTTPS!"
        fi

        LAN_AL_SSH_EN=`sqlite3 "${WEB_APP_DB_PATH}" "select lan_allow_ssh from service_setting where id=1"`
        if [ "${LAN_AL_SSH_EN}" = 0 ]
        then
            TMP_ACT="DROP"
            TMP_RULES="-p tcp -s 0/0 --sport 1024:65535 -d 0/0 --dport 22 -m state --state NEW -j ${TMP_ACT}"
            IPTBL_FILTER_RULES+="-A INPUT -i eth0 ${TMP_RULES}"
            IPTBL_FILTER_RULES+=$'\n'
        else
            echo "Enable LAN_AL_SSH!"
        fi
        ###=========================================================

    	IPTBL_FILTER_RULES+="-A FORWARD -i eth0 -o ${MLB_IFACE} -j ACCEPT"
    	IPTBL_FILTER_RULES+=$'\n'
        ###=======================for ipsec use================================================
        if [ "${DB_VPN_ACTIVE}" = 1 ]
        then
            for indx in ${DB_VPN_POSTROUTING_INDX[@]}
            do
                rule="select leftsubnet from vpn where id=${indx}"
                DB_VPN_LEFT_SUBNET=`sqlite3 "${WEB_APP_DB_PATH}" "${rule}"`
                IPTBL_NAT_RULES+="-A POSTROUTING -s ${DB_VPN_LEFT_SUBNET} -o ${MLB_IFACE} -m policy --dir out --pol ipsec -j ACCEPT"
                IPTBL_NAT_RULES+=$'\n'
                IPTBL_NAT_RULES+="-A POSTROUTING -s ${DB_VPN_LEFT_SUBNET} -o ${MLB_IFACE} -j MASQUERADE"
                IPTBL_NAT_RULES+=$'\n'
            done
        fi

        ###=======================for OpenVPN use==============================================
        if [ "${DB_OPENVPN_EN}" = 1 ]
        then
                IPTBL_NAT_RULES+="-A POSTROUTING -s ${DB_IF_ADDR_IP}/${IF_CIDR} -o tun+ -j MASQUERADE"
                IPTBL_NAT_RULES+=$'\n'
        fi
        ###=======================end==========================================================
    	IPTBL_NAT_RULES+="-A POSTROUTING -o ${MLB_IFACE} -j MASQUERADE"
    	IPTBL_NAT_RULES+=$'\n'

    	source gen-iptables-conf.sh

        MLB_PPP_NAT_PATH="${BACKUP_PATH}"

    done
fi
