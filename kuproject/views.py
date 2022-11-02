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
s_code = ""
corp_name = ""


def get(request):
    return render(request, 'index.html')


def main(request):
    news = newscrawling()
    (Kospi_chart_url, Kosdaq_chart_url, Kospi_scham, Kosdaq_scham, Kospi_f, Kosdaq_f, Kospi_trading,
     Kosdaq_trading) = priceindex()
    ex_name, ex_price = exchange()
    ex_dict = {}
    for i in range(5):
        ex_dict[ex_name[i]] = ex_price[i]
    return render(request, 'main.html', {'news': news,
                                         'Kospi_chart_url': Kospi_chart_url,
                                         'Kosdaq_chart_url': Kosdaq_chart_url,
                                         'Kospi_scham': Kospi_scham,
                                         'Kosdaq_scham': Kosdaq_scham,
                                         'Kospi_f': Kospi_f,
                                         'Kosdaq_f': Kosdaq_f,
                                         'Kospi_trading': Kospi_trading,
                                         'Kosdaq_trading': Kosdaq_trading,
                                         'ex_dict': ex_dict})


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
            prate = round((profit / (data[3] * data[4])) * 100, 2)
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
        sql1 = "select price, cnt from kuproject_stock_fav where user_id = '" + request.session[
            'u_id'] + "' and name = '" + input_fav_buy + "';"

        cursor.execute(sql1)
        data = cursor.fetchall()
        connection.commit()
        connection.close()

        oprice = data[0][0]
        ocnt = data[0][1]
        print(oprice, ocnt)

        if oprice == 0:
            tprice = price
            tcnt = cnt
        elif oprice is None:
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
            sql1 = "select price, cnt from kuproject_stock_fav where user_id = '" + request.session[
                'u_id'] + "' and name = '" + input_fav_sell + "';"

            cursor.execute(sql1)
            data = cursor.fetchall()

            oprice = data[0][0]
            ocnt = data[0][1]

            if ocnt < cnt:
                return render(request, 'alter_error.html')
            elif ocnt > cnt:
                tprice = (oprice * ocnt - price * cnt) // (ocnt - cnt)
                tcnt = ocnt - cnt
            else:
                tprice = "NULL"
                tcnt = "NULL"

            sql2 = "update kuproject_stock_fav set price = " + str(tprice) + ", cnt = " + str(
                tcnt) + " where user_id = '" + request.session['u_id'] + "' and name = '" + input_fav_sell + "';"
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
    global s_code
    global Corp_name
    if request.method == "GET":
        s_code = search_code(request.GET['hidden_corp_name'])
        Corp_name = request.GET['hidden_corp_name']
        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)

        summ = summary(s_code)
        return render(request, 'test2.html', {'ent': s_data['ent'],
                                              'date': s_data['ent_dict']['Date'],
                                              'close': s_data['ent_dict']['Close'],
                                              'eve': s_data['ent_dict']['eve'],
                                              'rate': s_data['ent_dict']['rate'],
                                              'color': s_data['ent_dict']['color'],
                                              'var': var,
                                              'corp_name': Corp_name,

                                              'summary': summ,
                                              })
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')


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
    if request.method == 'POST':
        test = request.POST['search_input']

        # -----------웹에서 입력한 검색어와 관련된 업체만 가져오기 -----------------
        # +++ 주의! com_df_rm 다시 호출하는 이유 : 검색 시 금융/보험 데이터 제거한 데이터프레임을 불러오기 때문
        com_df = pd.read_csv("y_finance_stockcode.csv")
        temp = com_df[(com_df['한글 종목명'].str.contains(test)) | (com_df['한글 종목명'].str.contains(test.upper()))][
            ['cd', '한글 종목명']].head()
        print(temp)

        result = json.dumps(temp.values.tolist())

        return HttpResponse(result)


def FS(request):
    if request.method == "GET":
        global s_code
        global Corp_name

        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)
        ifrs = crawl_ifrs(s_code)
        invest = tujaja(s_code)
        return render(request, 'FS.html', {'ent': s_data['ent'],
                                           'date': s_data['ent_dict']['Date'],
                                           'close': s_data['ent_dict']['Close'],
                                           'eve': s_data['ent_dict']['eve'],
                                           'rate': s_data['ent_dict']['rate'],
                                           'color': s_data['ent_dict']['color'],
                                           'var': var,
                                           'corp_name': Corp_name,
                                           'ifrs': ifrs,
                                           'invest': invest, })
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')


def investor(request):
    if request.method == "GET":
        global s_code
        global Corp_name

        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)
        ifrs = crawl_ifrs(s_code)
        invest = tujaja(s_code)
        return render(request, 'investor.html', {'ent': s_data['ent'],
                                                 'date': s_data['ent_dict']['Date'],
                                                 'close': s_data['ent_dict']['Close'],
                                                 'eve': s_data['ent_dict']['eve'],
                                                 'rate': s_data['ent_dict']['rate'],
                                                 'color': s_data['ent_dict']['color'],
                                                 'var': var,
                                                 'corp_name': Corp_name,
                                                 'ifrs': ifrs,
                                                 'invest': invest, })
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')


def news(request):
    if request.method == "GET":
        global s_code
        global Corp_name

        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)
        ifrs = crawl_ifrs(s_code)
        invest = tujaja(s_code)
        snews = stock_news(s_code)
        inv_name, inv_date, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg = invest_opinion(s_code)
        inv = {}
        i = 0
        for items in inv_name:
            i += 1
        for a in range(0, i):
            tmp = []
            tmp.append(inv_name[a])
            tmp.append(inv_date[a])
            tmp.append(target_prc[a])
            tmp.append(target_prc_bf[a])
            tmp.append(yoy[a])
            tmp.append(recom_cd[a])
            tmp.append(recom_cd_bf[a])
            inv[a] = tmp

        gs_title, gs_link, gs_info, gs_date = disclosure(s_code)
        gs = {}
        for i in range(0, len(gs_title)):
            tmp = []
            tmp.append(gs_link[i])
            tmp.append(gs_title[i])
            tmp.append(gs_info[i])
            tmp.append(gs_date[i])
            gs[i] = tmp

        return render(request, 'news.html', {'ent': s_data['ent'],
                                             'date': s_data['ent_dict']['Date'],
                                             'close': s_data['ent_dict']['Close'],
                                             'eve': s_data['ent_dict']['eve'],
                                             'rate': s_data['ent_dict']['rate'],
                                             'color': s_data['ent_dict']['color'],
                                             'var': var,
                                             'corp_name': Corp_name,
                                             'ifrs': ifrs,
                                             'invest': invest,
                                             'snews': snews,
                                             'inv': inv,
                                             'avg': avg,
                                             'gs': gs})
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')


def test3(request):
    if request.method == "GET":
        global s_code
        global Corp_name

        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)
        summ = summary(s_code)
        return render(request, 'test2.html', {'ent': s_data['ent'],
                                              'date': s_data['ent_dict']['Date'],
                                              'close': s_data['ent_dict']['Close'],
                                              'eve': s_data['ent_dict']['eve'],
                                              'rate': s_data['ent_dict']['rate'],
                                              'color': s_data['ent_dict']['color'],
                                              'var': var,
                                              'corp_name': Corp_name,
                                              'summary': summ,
                                              })
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')


def opin(request):
    if request.method == "GET":
        global s_code
        global Corp_name

        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)
        inv_name, inv_date, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg = invest_opinion(s_code)
        inv = {}
        i = 0
        for items in inv_name:
            i += 1
        for a in range(0, i):
            tmp = []
            tmp.append(inv_name[a])
            tmp.append(inv_date[a])
            tmp.append(target_prc[a])
            tmp.append(target_prc_bf[a])
            tmp.append(yoy[a])
            tmp.append(recom_cd[a])
            tmp.append(recom_cd_bf[a])
            inv[a] = tmp

        return render(request, 'opin.html', {'ent': s_data['ent'],
                                             'date': s_data['ent_dict']['Date'],
                                             'close': s_data['ent_dict']['Close'],
                                             'eve': s_data['ent_dict']['eve'],
                                             'rate': s_data['ent_dict']['rate'],
                                             'color': s_data['ent_dict']['color'],
                                             'var': var,
                                             'corp_name': Corp_name,
                                             'inv': inv,
                                             'avg': avg,
                                             })
    if request.method == "POST":
        s_name = request.POST['fav']
        et = search_code(s_name)
        s_code = list(et)[0][1].split(".")[0]
        if stock_fav.objects.filter(code=s_code).exists():
            return render(request, 'fav_exists.html')
        stock_fav.objects.create(user_id=request.session['u_id'], code=s_code, name=s_name)
        return render(request, 'fav_ok.html')


def commu(request):
    if request.method == "GET":
        global s_code
        global Corp_name
        code = list(s_code)[0][1].split(".")[0]
        s_data = chart_data(s_code, None)
        var = []
        x = list(s_data['ent_dict']['Date'].values())
        y = list(s_data['ent_dict']['Close'].values())
        var = zip(x, y)

        cursor = connection.cursor()
        sql1 = "select * from kuproject_stock_comm where code=" + code + " order by created_at desc;"
        cursor.execute(sql1)
        data = cursor.fetchall()

        sql2 = ""
        return render(request, 'community.html', {'ent': s_data['ent'],
                                                  'date': s_data['ent_dict']['Date'],
                                                  'close': s_data['ent_dict']['Close'],
                                                  'eve': s_data['ent_dict']['eve'],
                                                  'rate': s_data['ent_dict']['rate'],
                                                  'color': s_data['ent_dict']['color'],
                                                  'var': var,
                                                  'corp_name': Corp_name,
                                                  'code': code,
                                                  'data': data,})


def write(request):
    global s_code
    global corp_name
    if request.method == "POST":
        user_id = request.session['u_id']
        code = str(list(s_code)[0][1].split(".")[0])
        corp_name = corp_name
        title = request.POST['title']
        text = request.POST['text']

        cursor = connection.cursor()
        sql = "insert into kuproject_stock_comm(user_id, created_at, title, context, code, name, rep_cnt) VALUES('" + user_id + "', now(), '" + title + "','" + text + "','" + code + "','" + corp_name + "', 0);"

        cursor.execute(sql)
        data = cursor.fetchall()
        return render(request, 'write_ok.html')
    else:
        return render(request, 'write.html')


def comm_detail(request, pk):
    global s_code
    global corp_name
    u_id = request.session['u_id']

    code = str(list(s_code)[0][1].split(".")[0])
    cursor = connection.cursor()
    sql = 'select title, context, user_id, id from kuproject_stock_comm where id = ' + str(pk)
    cursor.execute(sql)
    data = cursor.fetchall()

    sql2 = 'select user_id, context, created_at, code, fk from kuproject_comment where fk=' + str(pk)
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    s_data = chart_data(s_code, None)
    var = []
    x = list(s_data['ent_dict']['Date'].values())
    y = list(s_data['ent_dict']['Close'].values())
    var = zip(x, y)
    return render(request, 'detail.html', {'ent': s_data['ent'],
                                                 'date': s_data['ent_dict']['Date'],
                                                 'close': s_data['ent_dict']['Close'],
                                                 'eve': s_data['ent_dict']['eve'],
                                                 'rate': s_data['ent_dict']['rate'],
                                                 'color': s_data['ent_dict']['color'],
                                                 'var': var,
                                                 'corp_name': Corp_name,
                                                 'code': code,
                                                 'data': data,
                                                 'u_id': u_id,
                                           'data2':data2, })


def comm_delete(request, pk):
    cursor = connection.cursor()
    sql = 'delete from kuproject_stock_comm where id =' + str(pk)
    cursor.execute(sql)
    return redirect('commu')


def comment_write(request, pk):
    global s_code
    code = str(list(s_code)[0][1].split(".")[0])
    u_id = request.session['u_id']
    context = request.POST.get('text')
    pk = str(pk)

    cursor = connection.cursor()
    sql = "insert into kuproject_comment(user_id, created_at, context, code, fk) values('" + u_id + "',now(),'" + context + "','" + str(code) + "','" + pk + "');"
    cursor.execute(sql)
    sql2 = "select rep_cnt from kuproject_stock_comm where id = " + pk
    cursor.execute(sql2)
    data = cursor.fetchall()

    cnt = data[0][0] + 1

    sql3 = "update kuproject_stock_comm set rep_cnt=" + str(cnt) + " where id =" + pk
    cursor.execute(sql3)
    return redirect(f'/detail/{pk}/',)


def board(request):
    if request.method == "GET":
        cursor = connection.cursor()
        sql1 = "select * from kuproject_community order by created_at desc;"
        cursor.execute(sql1)
        data = cursor.fetchall()

        sql2 = ""
        return render(request, 'board.html', {'data': data})


def board_write(request, pk):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        user_id = request.session['u_id']
        cursor = connection.cursor()
        sql = "insert into kuproject_community(user_id, created_at, title, context, rep_cnt) VALUES('" + user_id + "', now(), '" + title + "','" + text + "', 0);"

        cursor.execute(sql)
        data = cursor.fetchall()
        return render(request, 'write_ok.html')

    else:
        return render(request, 'write.html')


def board_detail(request, pk):
    u_id = request.session['u_id']

    cursor = connection.cursor()
    sql = 'select title, context, user_id, id from kuproject_community where id = ' + str(pk)
    cursor.execute(sql)
    data = cursor.fetchall()

    sql2 = 'select user_id, context, created_at, code, fk from kuproject_comment where fk=' + str(pk)
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    return render(request, 'board_detail.html', {'data': data,
                                           'u_id': u_id,
                                           'data2':data2, })


def board_delete(request, pk):
    cursor = connection.cursor()
    sql = 'delete from kuproject_community where id =' + str(pk)
    cursor.execute(sql)
    return redirect('board')


def board_comment_write(request, pk):
    u_id = request.session['u_id']
    context = request.POST.get('text')
    pk = str(pk)

    cursor = connection.cursor()
    sql = "insert into kuproject_comment(user_id, created_at, context, fk) values('" + u_id + "',now(),'" + context + "','" + pk + "');"
    cursor.execute(sql)
    sql2 = "select rep_cnt from kuproject_community where id = " + pk
    cursor.execute(sql2)
    data = cursor.fetchall()

    cnt = data[0][0] + 1

    sql3 = "update kuproject_community set rep_cnt=" + str(cnt) + " where id =" + pk
    cursor.execute(sql3)
    return redirect(f'/board_detail/{pk}/', )