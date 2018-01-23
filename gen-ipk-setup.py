#!/usr/bin/env python
import os
import sys
import glob
import logging
import init_env

log = logging.getLogger(__name__)

LOG_PATH = '/tmp/gen-ipk.log'


def genSetup(_OPKG_INSTALLATION, _OPKG_REMOVE):
    pkgDir = os.environ['MLB_DIR'] + '/pkg'
    if not os.path.isdir(pkgDir):
        log.error('The path {} not found.'.format(pkgDir))
    else:
        with open('{}/pkg/setup.sh'.format(os.environ['MLB_DIR']), 'w+') as f:
        # with open('/home/root/setup.sh', 'w+') as f:
            tmp = '#!/bin/sh' + '\n'
            tmp += '\n'
            tmp += _OPKG_INSTALLATION
            tmp += '\n'
            tmp += _OPKG_REMOVE
            tmp += '\n'

            f.write(tmp)


def main():
    OPKG_INSTALL_CMD = "/usr/bin/opkg install"
    OPKG_DELPKG_CMD = "rm -f"
    _OPKG_INSTALLATION = ""
    _OPKG_REMOVE = ""
    # _filters = "1.ipk 2.ipk 3.ipk"

    _OPKG_INSTALLATION += OPKG_INSTALL_CMD + ' '
    _OPKG_REMOVE += OPKG_DELPKG_CMD + ' '

    os.chdir(os.environ['MLB_DIR']+'/pkg')
    _filter = glob.glob('*.ipk')
    # os.chdir('/home/root/ipk/ipk-perl_for_ddns')
    # _filter = glob.glob('*.ipk')

    if not _filter:
        log.error('Not found any ipk file. Exited.')
        print "Not found any ipk file. Exited."
        sys.exit(1)

    for entry in _filter:
        log.info('IPK file found: {}'.format(entry))
        _OPKG_INSTALLATION += "{} ".format(entry)
        _OPKG_REMOVE += "{} ".format(entry)

    print('''*******
{}
{}
    '''.format(_OPKG_INSTALLATION, _OPKG_REMOVE))

    genSetup(_OPKG_INSTALLATION, _OPKG_REMOVE)


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename=LOG_PATH,
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
