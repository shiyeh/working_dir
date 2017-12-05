#!/usr/bin/python
import subprocess


def main():
    leases = []
    # _cmd = '/usr/bin/dumpleases -a'
    _cmd = 'cat leases.txt'
    ret = subprocess.check_output([_cmd], shell=True)
    tmp = ret.splitlines()[1:]
    print tmp[0]
    # with open('./leases.txt') as f:
    #     data = f.read()

    data = ret.split("\n")[1:]
    # print ret+'\n', data
    for i in data:
        if len(i.strip()) > 0:
            x = i.split()
            # print x

            k = {
                "Mac Address": x[0],
                "IP Address": x[1],
                "Host Name": x[2],
                "Expir": x[3]
            }
            leases.append(k)

    # print leases[0]["IP Address"]


if __name__ == '__main__':
    main()
