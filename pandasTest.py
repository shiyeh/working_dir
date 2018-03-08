#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 01:34:43
# @Author  : Leo Yeh (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd
import time
# %matplotlib inline
import fix_yahoo_finance as yf
yf.pdr_override()

ticker = '0050.TW'
start = '2000-01-01'
today = time.strftime("%Y-%m-%d")
print(today)

data = pdr.get_data_yahoo(ticker, start=start, end=today)
print(data)
c = data['Close']

c5 = c.rolling(5, min_periods=1).mean()
c60 = c.rolling(60, min_periods=1).mean()
c20 = c.rolling(20, min_periods=1).mean()
c['2016':].plot(label='c')
# c5['2015':].plot(label='c5')
# c20['2015':].plot(label='c20')
# c60['2015':].plot(label='c60')
plt.legend(loc='upper left')

plt.title(ticker)
plt.show()
