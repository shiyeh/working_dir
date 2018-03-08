#!/usr/bin/python
import sched, time, os

schedule = sched.scheduler(time.time, time.sleep)


def run_ntpd(inc):
    # 安排inc秒後再次運行自己，即周期運行
    schedule.enter(inc, 0, run_ntpd, (inc,))
    os.system('/usr/bin/python web-update-ntp-sync.py &')


def main(inc=30):
    # enter用來安排某事件的發生時間，從現在起第n秒開始啟動
    schedule.enter(0, 0, run_ntpd, (inc,))
    # 持續運行，直到計劃時間隊列變成空為止
    schedule.run()


if __name__ == '__main__':
    main()
