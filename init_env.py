#!/usr/bin/python
import os
import subprocess

# def init_env():
# cmd = '. /home/leo/working_dir/init-mlb-env.sh && env'
output = subprocess.check_output(
    ['bash', '-c', '. /home/leo/working_dir/init-mlb-env.sh && env'])
# out = subprocess.check_output(['ls', '-l'])
# print 'checkpoint----------------!\n'
# print output
# print 'checkpoint!\n'
# print out

for line in output.split('\n'):
    # print line

    if not line:
        # print 'This is not line.'
        continue

    try:
        key, value = line.split('=', 1)
    except Exception:
        continue

    # print 'key = ', os.environ.get(key)
    # print 'value = ', value

    if os.environ.get(key) != value:
        os.environ[key] = value

    with open('aaa.py', 'a+') as f:
        # f.write('#!/bin/python\n')
        print('os.environ["{}"]={}'.format(key, value))
        f.writelines('os.environ["{}"] = \"{}\"\n'.format(key, value))

    # print key + " = " + os.environ[key]
# def main():
#   init_env()

#   print 'DHCPD_IP_RANG_BGN = ', os.environ["DHCPD_IP_RANG_BGN"]
#   print 'DHCPD_IP_RANG_END = ', os.environ["DHCPD_IP_RANG_END"]
#   print 'IF_MASK_STR = ', os.environ["IF_MASK_STR"]

# if __name__ == '__main__':
#   main()
