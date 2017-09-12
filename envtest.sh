#!/bin/sh

export IPTBL_FILTER_RULES="This is in shell."
echo "IPTBL_FILTER_RULES = ${IPTBL_FILTER_RULES}"

export IPTBL_FILTER_RULES=`/usr/bin/python gen-iptables-rules.py`

echo "IPTBL_FILTER_RULES = ${IPTBL_FILTER_RULES}"
