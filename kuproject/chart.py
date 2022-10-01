import pandas as pd
from datetime import datetime, date, timedelta
from pykrx import stock
import math


def chart_data(ent, select_date=None):
    ent = list(ent)[0][1].split(".")[0]
    if (select_date != None):
        ent_df = stock.get_market_ohlcv_by_date(fromdate=select_date[0], todate=select_date[1], ticker=ent)

    else:
        e_date = datetime.now()
        s_date = e_date - timedelta(days=30)
        print(f"s_date .................: {s_date}")
        ent_df = stock.get_market_ohlcv_by_date(fromdate=s_date, todate=e_date, ticker=ent)
    ent_df = ent_df.reset_index()
    ent_df = ent_df.drop(['시가', '고가', '저가', '거래량'], axis=1)
    ent_df.columns = ['Date', 'Close']
    ent_df['Date'] = ent_df['Date'].astype('str')
    ent_dict = ent_df.to_dict()

    dfcp = ent_df.tail(2)
    rate_color = dfcp['Close'].values.tolist()
    ent_dict['eve'] = rate_color[0]
    ent_dict['today'] = rate_color[1]
    if (rate_color[1] - rate_color[0] < 0):
        ent_dict['rate'] = "fa fa-sort-desc"
        ent_dict['color'] = 'blue'
    else:
        ent_dict['rate'] = "fa fa-sort-asc"
        ent_dict['color'] = 'red'

    res = {'ent': ent, 'ent_dict': ent_dict}
    return res


def search_code(name):
    str = name
    com_df_srch = pd.read_csv('com_df_rm.csv',
                              dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str', 'stock_code_ori': 'str'},
                              parse_dates=['listed_date', '상장일'])
    temp = com_df_srch[(com_df_srch['한글 종목명'].str.contains(str)) | (com_df_srch['한글 종목명'].str.contains(str.upper()))][['yh_code', '한글 종목명']]
    #print(temp.values.tolist())
    return (temp.to_dict()['yh_code'].items())
