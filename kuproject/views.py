from django.shortcuts import render
from rest_framework.views import APIView

from kuproject.market import priceindex
from kuproject.news import newscrawling

from pykrx import stock
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.graph_objects as go

def get(request):
    return render(request,'index.html')

def main(request):
    news = newscrawling()
    return render(request,'main.html', {'news' : news})



def favorite(request):
    return render(request, 'favorite.html')

def nowstock(request):
    return render(request, 'nowstock.html')




def stockindex(request):
    return render(request,'stockindex.html')

def test2(request):
    return render(request,'test2.html')
def test3(request):
    return render(request,'test3.html')
def test4(request):
    return render(request,'test4.html')
def stockindex(request):
    (Kospi_chart_url, Kosdaq_chart_url, Kospi_scham, Kosdaq_scham, Kospi_f, Kosdaq_f, Kospi_trading, Kosdaq_trading) = priceindex()

    return render(request, 'stockindex.html', {'Kospi_chart_url' : Kospi_chart_url,
                                         'Kosdaq_chart_url' : Kosdaq_chart_url,
                                         'Kospi_scham' : Kospi_scham,
                                         'Kosdaq_scham' : Kosdaq_scham,
                                         'Kospi_f' : Kospi_f,
                                         'Kosdaq_f' : Kosdaq_f,
                                         'Kospi_trading' : Kospi_trading,
                                         'Kosdaq_trading' : Kosdaq_trading})



def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')

def test123(request):
    return render(request, '')