
import pandas as pd

import json
from django import template


def com_search_ajax(request):

    str = request.form.get('search_input')
    print(str)

    #-----------웹에서 입력한 검색어와 관련된 업체만 가져오기 -----------------
    # +++ 주의! com_df_rm 다시 호출하는 이유 : 검색 시 금융/보험 데이터 제거한 데이터프레임을 불러오기 때문
    com_df_srch =pd.read_csv('com_df_rm.csv',
                   dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str', 'stock_code_ori':'str'},
                   parse_dates=['listed_date', '상장일'])
    temp = com_df_srch[(com_df_srch['한글 종목명'].str.contains(str))|(com_df_srch['한글 종목명'].str.contains(str.upper()))][['yh_code', '한글 종목명']].head()
    print(temp.values.tolist())
    json.dumps(  temp.values.tolist()  )
    search = json.dumps(  temp.values.tolist()  )
    return search #리스트 형태로 데이터 전송

def form_submit_get(request):

    # get으로 전송된 데이터 받기
    hidden_stock_code = request.args.get("hidden_stock_code")
    hidden_corp_name = request.args.get("hidden_corp_name")


    origin_code= ori_code(hidden_stock_code) #우선주 종목코드를 보통주 종목코드로 바꿔주는 함수
    stock_code= hidden_stock_code[:-3] #yfinance 종목코드를 pykrx종목코드로 바꿔주는 함수

def ori_code(yh_code):
    origin_stock=com_df[com_df['yh_code']==yh_code]['stock_code_ori'].values[0]
    return origin_stock


com_df=pd.read_csv('com_df_rm.csv',
                   dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str', 'stock_code_ori':'str'},
                   parse_dates=['listed_date', '상장일'])