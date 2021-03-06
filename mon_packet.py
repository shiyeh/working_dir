#!/usr/bin/python
import sys, re, time, os
import logging

log = logging.getLogger(__name__)
maxdata = 50000  # kB
memfilename = '/tmp/mon_transdata.txt'
netcard = '/proc/net/dev'
nicname = 'ens33'
cal_intvl = 3  # seconds


def checkfile(filename):
    if os.path.isfile(filename):
        pass
    else:
        with open(filename, 'w') as f:
            f.write('0')


def get_net_data(nicname):
    nc = '/proc/net/dev'
    try:
        with open(nc, 'r') as fd:
            netcardstatus = False
            for line in fd.readlines():
                print line
                if line.find(nicname) > 0:
                    netcardstatus = True
                    field = line.split()
                    print field
                    recv = field[0].split(":")[1]
                    recv = recv or field[1]
                    send = field[9]
                    # print('recv= {} bytes, send= {} bytes'.format(recv, send))
    except Exception as e:
        raise e
    finally:
        fd.close()

    if not netcardstatus:
        print 'Please setup your netcard'
        sys.exit(1)
    return (float(recv), float(send))


def monfirst(filename):
    nowtime = time.strftime('%m-%d %H:%M', time.localtime(time.time()))
    sec = time.localtime().tm_sec
    print nowtime, sec
    if nowtime == '09-14 03:04':
        if sec < 10:
            with open(filename, 'w') as f:
                f.write('0')


def main():
    (recv, send) = get_net_data(nicname)
    checkfile(memfilename)
    monfirst(memfilename)
    # print('recv= {} send= {}'.format(recv, send))

    with open(memfilename, 'r') as lasttransdataopen:
        lasttransdata = lasttransdataopen.readline()

    totaltrans = float(lasttransdata) or 0
    # print 'totaltrans= {} kbytes'.format(totaltrans)

    while True:
        time.sleep(cal_intvl)
        (new_recv, new_send) = get_net_data(nicname)
        print('new_recv= {} kbytes, new_send= {} bytes'.format(new_recv, new_send))
        recvdata = (new_recv - recv) / 1024
        senddata = (new_send - send) / 1024
        print('recvdata= {} kbytes, senddata= {} kbytes'.format(recvdata, senddata))
        log.info('Data receive: {:.3f} kbytes, send= {:.3f} kbytes'.format(recvdata, senddata))
        # totaltrans += float(recvdata)
        # totaltrans += float(senddata)
        totaltrans = recvdata + senddata
        print 'totaltrans= {:.3f} kbytes'.format(totaltrans)
        log.info('Total transmision (Send + Receive)= {:.3f} kbytes'.format(totaltrans))

        with open(memfilename, 'w') as memw:
            memw.write(str(totaltrans) + '\n')

        if totaltrans >= maxdata:
            # print('shutdown.')
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/tmp/mon_net_packet.log',
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
