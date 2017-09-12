#!/bin/sh

source init-mlb-env.sh

TZ=`sqlite3 "${WEB_STAT_DB_PATH}" 'select utc_offset from system_info'`

if [ -f /etc/localtime ]
then
    unlink /etc/localtime
fi

case ${TZ} in
  "-12:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+12 /etc/localtime
      ;;
  "-11:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+11 /etc/localtime
      ;;
  "-10:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+10 /etc/localtime
      ;;
  "-09:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+9 /etc/localtime
      ;;
  "-08:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+8 /etc/localtime
      ;;
  "-07:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+7 /etc/localtime
      ;;
  "-06:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+6 /etc/localtime
      ;;
  "-05:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+5 /etc/localtime
      ;;
  "-04:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+4 /etc/localtime
      ;;
  "-03:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+3 /etc/localtime
      ;;
  "-02:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+2 /etc/localtime
      ;;
  "-01:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT+1 /etc/localtime
      ;;
  "+00:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/Universal /etc/localtime
      ;;
  "+01:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-1 /etc/localtime
      ;;
  "+02:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-2 /etc/localtime
      ;;
  "+03:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-3 /etc/localtime
      ;;
  "+04:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-4 /etc/localtime
      ;;
  "+05:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-5 /etc/localtime
      ;;
  "+06:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-6 /etc/localtime
      ;;
  "+07:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-7 /etc/localtime
      ;;
  "+08:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-8 /etc/localtime
      ;;
  "+09:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-9 /etc/localtime
      ;;
  "+10:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-10 /etc/localtime
      ;;
  "+11:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-11 /etc/localtime
      ;;
  "+12:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-12 /etc/localtime
      ;;
  "+13:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-13 /etc/localtime
      ;;
  "+14:00")
      echo "Time zone is ${TZ}."
      ln -s /usr/share/zoneinfo/Etc/GMT-14 /etc/localtime
      ;;
  "")
      ;;
  *)
      ;;
esac

source web-update-ntp-sync.sh
