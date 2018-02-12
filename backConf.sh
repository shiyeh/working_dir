#!/bin/sh
#source /opt/mlis/init-mlb-env.sh

#cd /opt/backup/mlis.old
_fileList=("/opt/mlis/conf/iptables*.ipv4.nat
            interfaces
	    udhcpd.conf
	    snmpd
	    snmpd.conf
	    openvpn/*
	    strongswan.conf
	    web_console
	   ")
for srcFile in ${_fileList}
do
    #touch /tmp/${srcFile}
    echo "FILE= ${srcFile}"

    #cp -a ${srcFile} /tmp/list
    #cp -a ${srcFile} ${MLB_CONF_DIR}
done

cp -rp /opt/backup/ipsec.d.old /etc/ipsec.d

cp -rp /tmp/app.db /opt/mlis/web_console/app/app.db

