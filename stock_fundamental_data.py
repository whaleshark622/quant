import pandas as pd
from mplfonts import use_font
import datetime
from sqlalchemy import create_engine
from ts import *
import calendar
import mysql.connector

pd.set_option('expand_frame_repr', False)
use_font('Noto Serif CJK SC')
conn = create_engine('mysql+pymysql://root:12345678@localhost/stock_fundamental_data')
cnx = mysql.connector.connect(user='root', password='12345678', host='localhost', database='stock_fundamental_data')
cursor = cnx.cursor()
# cursor.execute("USE fundamental_data")

# 获取第一天和最后一天
def getFirstAndLastDay(year, month):
    # 获取当前月的第一天的星期和当月总天数
    weekDay, monthCountDay = calendar.monthrange(year, month)
    # 获取当前月份第一天
    firstDay = datetime.date(year, month, day=1)
    # 获取当前月份最后一天
    lastDay = datetime.date(year, month, day=monthCountDay)
    # 返回第一天和最后一天
    return firstDay.strftime('%Y%m%d'), lastDay.strftime('%Y%m%d')


def get_fundamental_data_monthly(year, month):
    # 获取当月的交易日
    ts_code_list, ts_name_list = get_ts_code_name_list(exchange="SZSE", list_status="L")
    start, end = getFirstAndLastDay(year, month)
    cal = get_trade_cal(start, end)
    cal.sort()

    # 创建表
    print(f'\033[33mcreate if not exist {year}-{month}\033[0m')
    cursor.execute(f'CREATE TABLE IF NOT EXISTS `{year}-{month}` (\
          `id` INT AUTO_INCREMENT PRIMARY KEY,\
          `name` VARCHAR(15) COLLATE utf8mb4_unicode_ci,\
          `ts_code` VARCHAR(15) COLLATE utf8mb4_unicode_ci,\
          `trade_date` VARCHAR(15) COLLATE utf8mb4_unicode_ci,\
          `open` double DEFAULT NULL,\
          `high` double DEFAULT NULL,\
          `low` double DEFAULT NULL,\
          `close` double DEFAULT NULL,\
          `pre_close` double DEFAULT NULL,\
          `change` double DEFAULT NULL,\
          `pct_chg` double DEFAULT NULL,\
          `vol` double DEFAULT NULL,\
          `amount` double DEFAULT NULL,\
          `turnover_rate` double DEFAULT NULL,\
          `pe` double DEFAULT NULL,\
          `pe_ttm` double DEFAULT NULL,\
          `pb` double DEFAULT NULL,\
          `ps` double DEFAULT NULL,\
          `ps_ttm` double DEFAULT NULL,\
          `dv_ratio` double DEFAULT NULL,\
          `dv_ttm` double DEFAULT NULL,\
          `total_mv` double DEFAULT NULL,\
          `circ_mv` double DEFAULT NULL,\
           KEY `ts_code` (`ts_code`),\
           KEY `trade_date` (`trade_date`)\
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')

    # 获取每个交易日的信息
    for trade_date in cal:
        frames = list()
        basic = list()
        offset = 0
        while offset < len(ts_code_list):
            offset += 1000
            ts_code_list_chunk = ','.join(ts_code_list[offset - 1000:min(len(ts_code_list), offset)])
            frames.append(get_daily_data(ts_code=ts_code_list_chunk, trade_date=trade_date))
            basic.append(get_daily_basic_data(ts_code_list_chunk, trade_date))

        result = pd.concat([pd.concat(frames), pd.concat(basic)], axis=1).reset_index(drop=True)
        result = pd.concat([pd.DataFrame({'name': ts_name_list}), result], axis=1)
        print(f'insert {trade_date} fundamental data into {year}-{month}')
        result.to_sql(name=f'{year}-{month}', con=conn, if_exists='append', index=False)

    # 删除无效数据
    print(f'\033[33mclear {year}-{month} null data\033[0m')
    cursor.execute(f'delete from `{year}-{month}` where ts_code is NULL;')
