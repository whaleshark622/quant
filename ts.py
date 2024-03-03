import tushare as ts

token = '7f78dcbde213db3fdd61c030d15ac9def72eebb6def304df40d65618'


# 获取股票的交易代码和名字列表
def get_ts_code_name_list(limit="", offset="", exchange="", list_status=""):
    pro = ts.pro_api(token)
    df = pro.stock_basic(**{
        "ts_code": "",
        "name": "",
        "exchange": exchange,
        "market": "",
        "is_hs": "",
        "list_status": list_status,
        "limit": limit,
        "offset": offset
    }, fields=[
        "ts_code",
        "name",
        "industry",
        "market"
    ])
    return df['ts_code'].tolist(), df['name'].tolist()


# 获取日线数据
def get_daily_data(ts_code, trade_date="", start_date="", end_date=""):
    pro = ts.pro_api(token)
    return pro.daily(**{
        "ts_code": ts_code,
        "trade_date": trade_date,
        "start_date": start_date,
        "end_date": end_date,
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "pre_close",
        "change",
        "pct_chg",
        "vol",
        "amount"
    ])


def get_daily_basic_data(ts_code, trade_date, start_date="", end_date=""):
    pro = ts.pro_api(token)
    return pro.daily_basic(**{
        "ts_code": ts_code,
        "trade_date": trade_date,
        "start_date": start_date,
        "end_date": end_date,
    }, fields=[
        "turnover_rate",
        "pe",
        "pe_ttm",
        "pb",
        "ps",
        "ps_ttm",
        "dv_ratio",
        "dv_ttm",
        "total_mv",
        "circ_mv"
    ])


def get_index_daily_data(ts_code, trade_date='', start_date='', end_date='', limit='', offset=''):
    pro = ts.pro_api(token)
    return pro.index_dailybasic(**{
        "trade_date": trade_date,
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "offset": offset
    }, fields=[
        "ts_code",
        "trade_date",
        "total_mv",
        "float_mv",
        "total_share",
        "float_share",
        "free_share",
        "turnover_rate",
        "turnover_rate_f",
        "pe",
        "pe_ttm",
        "pb"
    ])


def get_fx_date(ts_code, trade_date="", start_date="", end_date="", exchange="", limit="", offset=""):
    pro = ts.pro_api(token)
    return pro.fx_daily(**{
        "ts_code": ts_code,
        "trade_date": trade_date,
        "start_date": start_date,
        "end_date": end_date,
        "exchange": exchange,
        "limit": limit,
        "offset": offset,
    }, fields=[
        "ts_code",
        "trade_date",
        "bid_open",
        "bid_close",
        "bid_high",
        "bid_low",
        "ask_open",
        "ask_close",
        "ask_high",
        "ask_low",
        "tick_qty"
    ])


def get_yc_cb(date='', start_date='', end_date='', curve_type='0'):
    pro = ts.pro_api(token)
    return pro.yc_cb(ts_code='1001.CB', curve_type=curve_type, trade_date=date, start_date=start_date,
                     end_date=end_date)


def get_us_tycr(date='', start_date='', end_date=''):
    pro = ts.pro_api(token)
    return pro.us_tycr(date=date, start_date=start_date, end_date=end_date)


def get_trade_cal(start_date, end_date):
    pro = ts.pro_api(token)
    df = pro.trade_cal(**{
        "exchange": "SSE",
        "start_date": start_date,
        "end_date": end_date,
        "is_open": "1",
    }, fields=[
        "exchange",
        "cal_date",
        "is_open",
        "pretrade_date"
    ])
    return df['cal_date'].tolist()
