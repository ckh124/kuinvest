import pymysql
from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse, redirect
from requests import auth
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection


from kuproject.market import *
from kuproject.news import *
from kuproject.chart import *
from kuproject.ifrs import *
from kuproject.models import *

from pykrx import stock
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.graph_objects as go
input_fav_buy = ""
input_fav_sell = ""

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
    cursor = connection.cursor()
    sql = "SELECT * FROM kuproject_stock_fav"
    result = cursor.execute(sql)
    datas = cursor.fetchall()

    connection.commit()
    connection.close()
    fav = []
    for data in datas:
        ent = search_code(data[2])
        tmp = chart_data(ent)
        profit = None
        prate = None
        if data[3] is not None:
            profit = (int(list(tmp['ent_dict']['Close'].values())[-1]) - data[4]) * data[3]
            prate = (profit / (data[3] * data[4])) * 100
        row = {'id': data[0],
               'code': data[1],
               'name': data[2],
               'cnt': data[3],
               'price': data[4],
               'close': list(tmp['ent_dict']['Close'].values())[-1],
               'prof': profit,
               'rate': prate}
        fav.append(row)

    return render(request, 'favorite.html', {'fav': fav})


def alter(request):
    global input_fav_buy
    global input_fav_sell
    for i in range(0, 1000):
        if request.POST.get('fav' + str(i) + '_buy'):
            input_fav_buy = request.POST.get('fav' + str(i) + '_buy')
            input_fav_sell = None
            break
        elif request.POST.get('fav' + str(i) + '_sell'):
            input_fav_sell = request.POST.get('fav' + str(i) + '_sell')
            input_fav_buy = None
            break
        else:
            continue

    if 'stockprice' in request.POST and input_fav_buy:
        price = int(request.POST['stockprice'])
        cnt = int(request.POST['stockamount'])
        print(price, cnt, request.session['u_id'], input_fav_buy, input_fav_sell)

        cursor = connection.cursor()
        sql1 = "select price, cnt from kuproject_stock_fav where user_id = '" + request.session['u_id'] + "' and name = '" + input_fav_buy + "';"

        cursor.execute(sql1)
        data = cursor.fetchall()
        connection.commit()
        connection.close()

        oprice = data[0][0]
        ocnt = data[0][1]
        print(oprice, ocnt)

        if oprice is None:
            tprice = price
            tcnt = cnt
        else:
            tprice = (oprice * ocnt + price * cnt) // (ocnt + cnt)
            tcnt = ocnt + cnt

        print(tprice, tcnt)
        cursor = connection.cursor()
        sql2 = "update kuproject_stock_fav set price = " + str(tprice) + ", cnt = " + str(tcnt) + " where user_id = '" + \
               request.session['u_id'] + "' and name = '" + input_fav_buy + "';"
        cursor.execute(sql2)
        cursor.fetchall()

        connection.commit()
        connection.close()
        return render(request, 'alter_ok.html')




    if 'stockprice' in request.POST and input_fav_sell:
        price = int(request.POST['stockprice'])
        cnt = int(request.POST['stockamount'])
        print(price, cnt, request.session['u_id'], input_fav_buy, input_fav_sell)
        try:
            cursor = connection.cursor()
            sql1 = "select price, cnt from kuproject_stock_fav where user_id = '" + request.session['u_id'] + "' and name = '" + input_fav_sell + "';"

            cursor.execute(sql1)
            data = cursor.fetchall()

            oprice = data[0][0]
            ocnt = data[0][1]

            if ocnt < cnt:
                return render(request, 'alter_error.html')
            else:
                tprice = (oprice*ocnt - price*cnt)//(ocnt+cnt)
                tcnt = ocnt-cnt

            sql2 = "update kuproject_stock_fav set price = " + str(tprice) + ", cnt = " + str(tcnt) + " where user_id = '" + request.session['u_id'] + "' and name = '" + input_fav_sell + "';"
            cursor.execute(sql2)

            connection.commit()
            connection.close()
            return render(request, 'alter_ok.html')

        except:
            connection.rollback()
            print("Failed connecting DB")

    return render(request, 'alter.html', {'input_buy': input_fav_buy,
                                          'input_sell': input_fav_sell})





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
        invest = tujaja(s_code)
        return render(request, 'test2.html', {'ent': s_data['ent'],
                                              'date': s_data['ent_dict']['Date'],
                                              'close': s_data['ent_dict']['Close'],
                                              'eve': s_data['ent_dict']['eve'],
                                              'rate': s_data['ent_dict']['rate'],
                                              'color': s_data['ent_dict']['color'],
                                              'var': var,
                                              'corp_name': request.GET['hidden_corp_name'],
                                              'ifrs': ifrs,
                                              'invest': invest,})
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')





def test3(request):

        return render(request, 'test3.html')

def test4(request):
    return render(request, 'test4.html')




def login(request):
    if request.method == "POST":
        id = request.POST['id']
        pw = request.POST['pw']
        context = {}
        if user.objects.filter(id=id).exists():
            getUser = user.objects.get(id=id)
            if check_password(pw, getUser.pw):
                request.session['u_id'] = id
                return main(request)
        else:
            return render(request, 'login_error.html')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login.html')

def register(request):
    if request.method == "POST":
        if user.objects.filter(id=request.POST['id']).exists():  # 아이디 중복 체크
            return render(request, 'id_error.html')
        if user.objects.filter(email=request.POST['email']).exists():  # 이메일 중복 체크
            return render(request, 'email_error.html')
        if request.POST['pw'] == request.POST['pw2']:
            member = user.objects.create(
                id=request.POST['id'], email=request.POST['email'], pw=make_password(request.POST['pw']))
            return render(request, 'register_ok.html')
    return render(request, 'register.html')


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
