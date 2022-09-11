from django.shortcuts import render
from rest_framework.views import APIView

from kuproject.market import priceindex
from kuproject.news import newscrawling


def get(request):
    return render(request,'index.html')

def main(request):
    news = newscrawling()
    return render(request,'main.html', {'news' : news})

def mystock(request):
    return render(request,'mystock.html')
def SCinput(request):
    return render(request,'SCinput.html')

def favorite(request):
    return render(request, 'favorite.html')

def nowstock(request):
    return render(request, 'nowstock.html')

def order(request):
    return render(request,'order.html')

def profit(request):
    return render(request,'profit.html')

def stockindex(request):
    return render(request,'stockindex.html')
def test1(request):
    return render(request,'test1.html')
def test2(request):
    return render(request,'test2.html')
def test3(request):
    return render(request,'test3.html')
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



