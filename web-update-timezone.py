#!/usr/bin/python

import os
import sys
import sqlite3
import subprocess
import init_env


def syncTimeZone(tz):
    if os.path.isfile("/etc/localtime"):
        print 'File is exist.'
        os.system("unlink /etc/localtime")
    else:
        print 'File is not exist.'

    if tz == "-12:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+12 /etc/localtime")
    elif tz == "-11:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+11 /etc/localtime")
    elif tz == "-10:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+10 /etc/localtime")
    elif tz == "-09:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+9 /etc/localtime")
    elif tz == "-08:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+8 /etc/localtime")
    elif tz == "-07:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+7 /etc/localtime")
    elif tz == "-06:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+6 /etc/localtime")
    elif tz == "-05:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+5 /etc/localtime")
    elif tz == "-04:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+4 /etc/localtime")
    elif tz == "-03:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+3 /etc/localtime")
    elif tz == "-02:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+2 /etc/localtime")
    elif tz == "-01:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT+1 /etc/localtime")
    elif tz == "+00:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/Universal /etc/localtime")
    elif tz == "+01:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-1 /etc/localtime")
    elif tz == "+02:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-2 /etc/localtime")
    elif tz == "+03:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-3 /etc/localtime")
    elif tz == "+04:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-4 /etc/localtime")
    elif tz == "+05:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-5 /etc/localtime")
    elif tz == "+06:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-6 /etc/localtime")
    elif tz == "+07:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-7 /etc/localtime")
    elif tz == "+08:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-8 /etc/localtime")
    elif tz == "+09:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-9 /etc/localtime")
    elif tz == "+10:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-10 /etc/localtime")
    elif tz == "+11:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-11 /etc/localtime")
    elif tz == "+12:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-12 /etc/localtime")
    elif tz == "+13:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-13 /etc/localtime")
    elif tz == "+14:00":
        print tz
        os.system("ln -s /usr/share/zoneinfo/Etc/GMT-14 /etc/localtime")
    else:
        print "Something error."
        sys.exit(1)


def main():
    if 'WEB_STAT_DB_PATH' in os.environ:
        con = sqlite3.connect(os.environ['WEB_STAT_DB_PATH'])
        cur = con.cursor()

        tzTmp = cur.execute("select utc_offset from system_info;").fetchone()
        con.close()

        syncTimeZone(tz=str(tzTmp[0]))

    ntpSyncFile = os.environ["MLB_DIR"] + "/web-update-ntp-sync.py"
    if os.path.isfile(ntpSyncFile):
        subprocess.check_call(['/usr/bin/python', ntpSyncFile])


if __name__ == '__main__':
    main()
