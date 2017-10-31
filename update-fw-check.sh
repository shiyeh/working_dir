#!/bin/sh

source /opt/mlis/init-mlb-env.sh

DATE=`date "+%Y%m%d"`
log_path="/opt/log/fwUpdateTmp.log"
echo "### This is log file when updating firmware." > ${log_path}
echo "### DATE: ${DATE}" >> ${log_path}

if [ -f /tmp/*.fw ]
then
    fw_name=`ls /tmp/*.fw`
    basename=`basename ${fw_name}`
    echo "`date "+%T"` [INFO] Start to check firmware. FW version: ${basename}" >> ${log_path}
    echo "`date "+%T"` [INFO] Decompression file" >> ${log_path}
    tar -xvpf ${fw_name} -C /tmp >> ${log_path}
    md5_original=`cat /tmp/md5`
    md5_file=`md5sum /tmp/mlis.tar.gz | awk '{ print $1 }'`
    echo "`date "+%T"` [INFO] Untar finished." >> ${log_path}
    echo "`date "+%T"` [INFO] Original MD5 is ${md5_original}" >> ${log_path}
    echo "`date "+%T"` [INFO] New MD5 is ${md5_file}" >> ${log_path}
else
    echo "`date "+%T"` [ERROR] FW file not found." >> ${log_path}
    rm -f /tmp/*.fw
    exit 1
fi

# ===================kill process before update FW===========================
kill_list=()
pid_of_ppp_on_boot=`ps | grep {ppp_on_boot} | awk '{ print $1 }' | head -n 1`
kill_list+=(${pid_of_ppp_on_boot})
pid_of_serial_config=`pidof serial-config`
kill_list+=(${pid_of_serial_config})

for pid in ${kill_list[@]}
do
    echo "`date "+%T"` [INFO] Kill process before update FW." >> ${log_path}
	kill -9 ${pid}
done
#============================================================================


if [ $md5_original != $md5_file ]
then
    rm -f /tmp/*.fw /tmp/md5 /tmp/mlis.tar.gz
    echo "`date "+%T"` [ERROR] Firmware update not start cause MD5 is not the same." >> ${log_path}
	exit 1
fi
exit 0
