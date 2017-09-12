#!/bin/sh

PKTLOSS=$(ping -c2 www.pool.ntp.org| grep "packet loss" |awk '{print $6}')
# PKTLOSS=$(ping -c2 www.pool.ntp.org| grep "packet loss" |awk '{print $7}')

if [ "${PKTLOSS}" == "0%" ]; then
   ntpd -g -q pool.ntp.org
   
   if [ $? -eq 0 ]; then
       hwclock -w
       echo "SYNC successfully."
   else
       echo "FAILED SYNC. Error code: $?" && exit 1
   fi
else
   echo "ERROR: Network is unreachable." && exit 1
fi

