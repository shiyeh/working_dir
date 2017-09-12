from multiprocessing import Process
import os
from keep_alive import KeepAlive

if __name__ == '__main__':
    KeepAlive()

# def info(title):
#     print title
#     print 'module name:', __name__
#     if hasattr(os, 'getppid'):  # only available on Unix
#         print 'parent process:', os.getppid()
#     print 'process id:', os.getpid()

# def f(name):
#     info('function f')
#     print 'hello', name

# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

