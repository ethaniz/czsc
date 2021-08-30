# -*- coding:utf8 -*-

from czsc.data.jq import *
set_token('13981945021', '945021')
print('joinquant剩余调用次数: {}'.format(get_query_count()))

from datetime import datetime
import czsc
#from czsc.factors import CzscTrader
from czsc.data.jq import JqCzscTrader as CzscTrader

print(czsc.__version__)
#assert czsc.__version__ == '0.7.0'

ct = CzscTrader(symbol='600166.XSHE', end_date=datetime.now())
ct.open_in_browser()

#ct = GmCzscTrader("SZSE.002414", end_dt='2021-06-25 14:38:00+08:00')
#ct.open_in_browser()