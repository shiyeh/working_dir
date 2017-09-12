#!/bin/sh

log_path=/tmp/fw_update.log
fw_name=`ls /tmp/*.fw`
basename=`basename ${fw_name}`
echo "Start to firmware update. FW version: ${basename}" > ${log_path}
echo "successful." >> ${log_path}
