from stock_fundamental_data import *

year = 2023

if __name__ == '__main__':
    for year in range(2014, 2024):
        for month in range(1, 12 + 1):
            print(f'\033[34mget {year}-{month} fundamental data\033[0m')
            get_fundamental_data_monthly(year, month)
            print(f'\033[34mget {year}-{month} fundamental data done\033[0m')
