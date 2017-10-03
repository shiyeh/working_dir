#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-03 06:46:06
# @Author  : Leo Yeh (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os

DB_IF_MASK_STR = '255.255.240.0'

IF_CIDR = sum([bin(int(x)).count("1")
    for x in DB_IF_MASK_STR.split(".")])

print IF_CIDR


# if __name__ == '__main__':
#     f = genTable('leo', 18)
#     f.blockSSH()
#     f.blockHttp()
