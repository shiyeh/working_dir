#!/bin/sh

source init-mlb-env.sh
log_path=`ls /opt/log/fwUpdateTmp.log`

sleep 1
if [ -f "/tmp/mlis.tar.gz" ]
then
    echo "`date "+%T"` [INFO] Remove all files under ${MLB_DIR}" >> ${log_path}
    rm -rf ${MLB_DIR}/*
    echo "`date "+%T"` [INFO] Start to update firmware." >> ${log_path}
    tar -xvpf /tmp/mlis.tar.gz -C / >> ${log_path}

    source web-update-all.sh

    echo "`date "+%T"` [INFO] Reboot system." >> ${log_path}
    
    DATE=`date "+%Y%m%d"`
    log_bak_path="/opt/log/fwUpdate-${DATE}.log"
    /bin/cp ${log_path} ${log_bak_path}
    /bin/rm ${log_path}

    sync
    reboot
    exit 0
fi
echo "`date "+%T"` [ERROR] Cannot found FW file." >> ${log_path}
exit 1
