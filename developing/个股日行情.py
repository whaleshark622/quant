import numpy as np
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import Kline
from mplfonts import use_font
use_font('Noto Serif CJK SC')
pro = ts.pro_api('7f78dcbde213db3fdd61c030d15ac9def72eebb6def304df40d65618')

# 获取平安银行日行情数据
pa = pro.daily(**{
    "ts_code": "000001.SZ",
    "trade_date": "",
    "start_date": 20230128,
    "end_date": 202340128,
    "offset": "",
    "limit": ""
})

pa.index = pd.to_datetime(pa.trade_date)
pa = pa.sort_index()
v1 = list(pa.loc[:, ['open', 'close', 'low', 'high']].values)
v0 = list(pa.index.strftime('%Y%m%d'))
kl = Kline()
kl.add("", v0, v1,
       is_datazoom_show=True,
       mark_line=["average"],
       mark_point=["max", "min"],
       mark_point_symbolsize=60,
       mark_line_valuedim=['highest', 'lowest'],
)
# kline.render("上证指数图.html")
kl.render()
