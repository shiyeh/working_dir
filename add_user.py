#!/usr/bin/python
import os
import sys
from subprocess import Popen, PIPE
import logging

log = logging.getLogger(__name__)


def delUser(userName):
    try:
        log.info('Delete user: %s now...' % userName)
        p1 = Popen(['/usr/sbin/userdel', '-r', userName], stdout=PIPE, stderr=PIPE)
        out, err = p1.communicate()
        if p1.returncode != 0:
            raise Exception(err.strip())
    except Exception as e:
        log.exception(e)
    else:
        log.info('Delete user: %s successfully.' % userName)


def modUserProfile(userName):
    filePath = '/home/%s/.profile' % (userName)

    if os.path.isfile(filePath):
        # Backup the profile if it exist.
        os.system('/bin/cp %s %s.bak' % (filePath, filePath))

        ''' When the user login, it need to call 'cli' command
            To do this, we must modify the user profile. '''
        try:
            with open(filePath, 'a+') as f:
                tmp = '\n'
                tmp += 'if [ -f /opt/mlis/web_console/cli/main.py ]; then\n'
                tmp += '    /usr/bin/python /opt/mlis/web_console/cli/main.py\n'
                tmp += '    exit 0\n'
                tmp += 'fi\n'

                f.write(tmp)

        except Exception as e:
            log.exception(e)
        finally:
            f.close()
    else:
        log.debug('The file %s is not found.' % (filePath))


def addUser(userName, passWord):
    homePath = '/home/%s' % (userName)

    p1 = Popen(['/usr/sbin/useradd', '-m', '-d', homePath, userName], stdout=PIPE, stderr=PIPE)
    out, err = p1.communicate()
    if p1.returncode != 0:
        raise Exception(err.strip())

    p2 = Popen(['/usr/bin/passwd', userName], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p2.communicate(passWord + '\n' + passWord + '\n')
    if p2.returncode != 0:
        raise Exception(err.strip())


def main():
    if len(sys.argv) != 3:
        print("""Usage:
1) Create user:
    /usr/bin/python add_user.py <username> <password>
2) Delete user:
    /usr/bin/python add_user.py del <username>
            """)
        return False

    # Delete user
    if (sys.argv[1] == 'del') & (sys.argv[2] != ''):
        delUser(userName=sys.argv[2])
        return True

    # Try to add user
    try:
        addUser(userName=sys.argv[1], passWord=sys.argv[2])

    except Exception as e:
        log.exception(e)
    else:
        log.debug('Add user: %s successfully.' % (sys.argv[1]))

        # If user created successful, do modUserProfile.
        modUserProfile(userName=sys.argv[1])
    finally:
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, filename='/tmp/addUser.log',
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
