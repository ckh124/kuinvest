from django.shortcuts import render
from rest_framework.views import APIView

from kuproject.market import priceindex
from kuproject.news import newscrawling
from kuproject.chart import chart_data, search_code

from pykrx import stock
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.graph_objects as go

def get(request):
    return render(request,'index.html')

def main(request):
    news = newscrawling()
    (Kospi_chart_url, Kosdaq_chart_url, Kospi_scham, Kosdaq_scham, Kospi_f, Kosdaq_f, Kospi_trading, Kosdaq_trading) = priceindex()
    return render(request,'main.html', {'news' : news,
                                        'Kospi_chart_url' : Kospi_chart_url,
                                        'Kosdaq_chart_url' : Kosdaq_chart_url,
                                        'Kospi_scham' : Kospi_scham,
                                        'Kosdaq_scham' : Kosdaq_scham,
                                        'Kospi_f' : Kospi_f,
                                        'Kosdaq_f' : Kosdaq_f,
                                        'Kospi_trading' : Kospi_trading,
                                        'Kosdaq_trading' : Kosdaq_trading})



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
    if request.method == "POST":
        s_code = search_code(request.POST['user_input'])
        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)

        return render(request, 'test2.html', {'ent': s_data['ent'],
                                              'date': s_data['ent_dict']['Date'],
                                              'close': s_data['ent_dict']['Close'],
                                              'eve': s_data['ent_dict']['eve'],
                                              'rate': s_data['ent_dict']['rate'],
                                              'color': s_data['ent_dict']['color'],
                                              'var': var},)

def test3(request):
    return render(request, 'test3.html')
def test4(request):
    return render(request, 'test4.html')




def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')

