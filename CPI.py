import tushare as ts
import matplotlib.pyplot as plt

# 初始化pro接口
pro = ts.pro_api('7f78dcbde213db3fdd61c030d15ac9def72eebb6def304df40d65618')

# 拉取数据
df = pro.cn_cpi(**{
    "m": "",
    "start_m": "",
    "end_m": "",
    "limit": "",
    "offset": ""
}, fields=[
    "month",
    "nt_val",
    "nt_yoy",
    "nt_mom",
    "nt_accu",
    "town_val",
    "town_yoy",
    "town_mom",
    "town_accu",
    "cnt_val",
    "cnt_yoy",
    "cnt_mom",
    "cnt_accu"
])
print(df)


