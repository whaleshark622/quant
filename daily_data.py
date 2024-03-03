from ts import *
import datetime
import pandas as pd

pd.set_option('expand_frame_repr', False)
index = {
    "沪深300": "000300.SH",
    "上证指数": "000001.SH",
    "中证500": "000905.SH",
    "创业指板": "399006.SZ",
}

trade_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
last_trade_date = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y%m%d')
print('trade_date: {}'.format(trade_date))

# 汇率
USD_CNY = get_fx_date(ts_code="USDCNH.FXCM", trade_date=last_trade_date).iloc[0]['bid_open']
USD_HKD = get_fx_date(ts_code="USDHKD.FXCM", trade_date=last_trade_date).iloc[0]['bid_open']
HKD_CNY = USD_CNY / USD_HKD
print('USD/CNY: {}, USD/HKD: {}, HKD/CNY: {}'.format(
    round(USD_CNY, 3),
    round(USD_HKD, 3),
    round(HKD_CNY, 3),
))

yc_cb = get_yc_cb(date=trade_date, curve_type="0")
y1_yield, y10_yield = 0.0, 0.0
for row in yc_cb.itertuples():
    curve_term = getattr(row, "curve_term")
    if curve_term == 1.0:
        y1_yield = getattr(row, "_6")
    elif curve_term == 10.0:
        y10_yield = getattr(row, "_6")
print('中国1年期国债利率: {}, 10年期国债利率: {}'.format(y1_yield, y10_yield))

us_tyrc = get_us_tycr(date=last_trade_date).iloc[0]
print('美国1年期国债利率: {}, 10年期国债利率: {}'.format(us_tyrc['y1'], us_tyrc['y10']))

for ts_name, ts_code in index.items():
    df = get_index_daily_data(ts_code=ts_code, trade_date=trade_date)
    pe = df.iloc[0]['pe']
    pb = df.iloc[0]['pb']
    roe = round(pb / pe, 3)
    roe_div_pb = round(roe / pb, 3)
    print('{}  PE: {}, PB {}, ROE: {}, ROE/PB: {}, turnover: {}'.format(
        ts_name,
        pe,
        pb,
        roe,
        roe_div_pb,
        df.iloc[0]['turnover_rate'],
    ))
