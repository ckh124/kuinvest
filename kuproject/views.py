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
    if request.POST:
        kospi_list = pd.DataFrame({'종목코드': stock.get_market_ticker_list(market="KOSPI")})
        kosdaq_list = pd.DataFrame({'종목코드': stock.get_market_ticker_list(market="KOSDAQ")})

        stock_list = pd.concat([kospi_list, kosdaq_list], axis=0, ignore_index=True)
        stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
        stock_list_etf = pd.DataFrame({'종목코드': stock.get_etf_ticker_list(datetime.today().strftime("%Y%m%d"))})
        stock_list_etf['종목명'] = stock_list_etf['종목코드'].map(lambda x: stock.get_etf_ticker_name(x))

        plt.rcParams["font.family"] = "Malgun Gothic"
        stock_code=request.POST['user_input']
        stock_from = (datetime.today() - timedelta(days=50)).strftime('%Y%m%d')
        stock_to = datetime.today().strftime('%Y%m%d')
        stock_name = stock_list.loc[stock_list['종목코드'] == stock_code, '종목명']
        if str(stock_name.values) == '[]':
            stock_name = stock_list_etf.loc[stock_list_etf['종목코드'] == stock_code, '종목명']

        df = stock.get_market_ohlcv_by_date(fromdate="20220101", todate=stock_to, ticker=stock_code, freq="d")

        df = df.rename(columns={'시가': 'Open', '고가': 'High', '저가': 'Low', '종가': 'Close', '거래량': 'Volume'})
        df['Close'] = df['Close'].apply(pd.to_numeric, errors="coerce")
        df['ma20'] = df['Close'].rolling(window=20).mean()
        df['stddev'] = df['Close'].rolling(window=20).std()
        df['upper'] = df['ma20'] + 2 * df['stddev']
        df['lower'] = df['ma20'] - 2 * df['stddev']

        for i in range(len(df)):
            if df['Open'].iloc[i] == 0:
               df['Open'].iloc[i] = df['Close'].iloc[i]
               df['High'].iloc[i] = df['Close'].iloc[i]
               df['Low'].iloc[i] = df['Close'].iloc[i]


        candle = go.Candlestick(x=df.index)
        candle = go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='red',
            decreasing_line_color='blue')
        fig = go.Figure(data=candle)

        fig.write_html("test4.html")
        plt.show()

    return render(request,'test1.html')
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