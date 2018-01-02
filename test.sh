#!/bin/sh

read -p "Please input 1.tcp 2.udp 3.tcp/udp: " DB_NAT_PORTFW_PROTOCOL

case ${DB_NAT_PORTFW_PROTOCOL} in
    "tcp")
#        IPTBL_FILTER_RULES+="-A FORWARD -d ${DB_NAT_PORTFW_IP}/32 -p ${DB_NAT_PORTFW_PROTOCOL} -m ${DB_NAT_PORTFW_PROTOCOL} --dport ${DB_NAT_PORTFW_INTERNAL} -m state --state NEW,RELATED,ESTABLISHED -j ACCEPT"
#        IPTBL_FILTER_RULES+=$'\n'
#        IPTBL_NAT_RULES+="-A PREROUTING -i ${MLB_IFACE} -p ${DB_NAT_PORTFW_PROTOCOL} -m ${DB_NAT_PORTFW_PROTOCOL} --dport ${DB_NAT_PORTFW_PUBLIC} -j DNAT --to-destination ${DB_NAT_PORTFW_IP}:${DB_NAT_PORTFW_INTERNAL}"
#        IPTBL_NAT_RULES+=$'\n'
         echo "this is tcp"
    ;;
    "udp")
         echo "this is udp"
    ;;
    "tcp/udp")
         echo "this is tcp/udp"
    ;;
esac
