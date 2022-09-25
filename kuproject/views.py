from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView

from kuproject.market import priceindex, exchange
from kuproject.news import newscrawling
from kuproject.chart import chart_data, search_code
from kuproject.ifrs import crawl_ifrs

from pykrx import stock
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.graph_objects as go

def get(request):
    return render(request,'index.html')

def main(request):
    news = newscrawling()
    (Kospi_chart_url, Kosdaq_chart_url, Kospi_scham, Kosdaq_scham, Kospi_f, Kosdaq_f, Kospi_trading, Kosdaq_trading) = priceindex()
    ex_name, ex_price = exchange()
    ex_dict = {}
    for i in range(5):
        ex_dict[ex_name[i]] = ex_price[i]
    return render(request,'main.html', {'news' : news,
                                        'Kospi_chart_url' : Kospi_chart_url,
                                        'Kosdaq_chart_url' : Kosdaq_chart_url,
                                        'Kospi_scham' : Kospi_scham,
                                        'Kosdaq_scham' : Kosdaq_scham,
                                        'Kospi_f' : Kospi_f,
                                        'Kosdaq_f' : Kosdaq_f,
                                        'Kospi_trading' : Kospi_trading,
                                        'Kosdaq_trading' : Kosdaq_trading,
                                        'ex_dict' : ex_dict})



def favorite(request):
    return render(request, 'favorite.html')

def nowstock(request):
    return render(request, 'nowstock.html')




def stockindex(request):
    return render(request, 'stockindex.html')
def test1(request):
    if request.method == "GET":
        return render(request, 'test1.html')


def test2(request):
    if request.method == "GET":
        s_code = search_code(request.GET['hidden_corp_name'])
        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)
        ifrs = crawl_ifrs(s_code)
        return render(request, 'test2.html', {'ent': s_data['ent'],
                                              'date': s_data['ent_dict']['Date'],
                                              'close': s_data['ent_dict']['Close'],
                                              'eve': s_data['ent_dict']['eve'],
                                              'rate': s_data['ent_dict']['rate'],
                                              'color': s_data['ent_dict']['color'],
                                              'var': var,
                                              'corp_name': request.GET['hidden_corp_name'],
                                              'ifrs': ifrs},)



def test3(request):

        return render(request, 'test3.html', {'ifrs' : ifrs})

def test4(request):
    return render(request, 'test4.html')




def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')


def com_search_ajax(request):

    if request.method =='POST':
     test = request.POST['search_input']


    #-----------웹에서 입력한 검색어와 관련된 업체만 가져오기 -----------------
    # +++ 주의! com_df_rm 다시 호출하는 이유 : 검색 시 금융/보험 데이터 제거한 데이터프레임을 불러오기 때문
     com_df = pd.read_csv("y_finance_stockcode.csv")
     temp = com_df[(com_df['한글 종목명'].str.contains(test)) | (com_df['한글 종목명'].str.contains(test.upper()))][['cd', '한글 종목명']].head()
     print(temp)

     result = json.dumps(  temp.values.tolist()  )


     return HttpResponse(result)
