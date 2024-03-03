# 先引入后面分析、可视化等可能用到的库
import numpy as np
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from mplfonts import use_font

use_font('Noto Serif CJK SC')

# 设置token
pro = ts.pro_api('7f78dcbde213db3fdd61c030d15ac9def72eebb6def304df40d65618')


def get_index_data(indexs):
    '''indexs是字典格式'''
    index_data = {}
    for name, code in indexs.items():
        df = pro.index_daily(
            ts_code=code,
            start_date=20230128,
            end_date=20240128,
        )
        df.index = pd.to_datetime(df.trade_date)
        index_data[name] = df.sort_index()
    return index_data


# 获取常见股票指数行情
indexs = {'上证综指': '000001.SH',
          '深证成指': '399001.SZ',
          '沪深300': '000300.SH',
          '创业板指': '399006.SZ',
          '上证50': '000016.SH',
          '中证500': '000905.SH',
          '中小板指': '399005.SZ',
          '上证180': '000010.SH'}
index_data = get_index_data(indexs)

# 对股价走势进行可视化分析
subjects = list(index_data.keys())
# 每个子图的title
plot_pos = [421, 422, 423, 424, 425, 426, 427, 428]  # 每个子图的位置
new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2',
              '#7f7f7f', '#bcbd22', '#17becf']

fig = plt.figure(figsize=(16, 18))

fig.suptitle('A股股指走势')
for pos in np.arange(len(indexs)):
    ax = fig.add_subplot(421+pos)
    y_data = index_data[subjects[pos]]['close']
    b = ax.plot(y_data, color=new_colors[pos])
    ax.set_title(subjects[pos])

plt.show()
