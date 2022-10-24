import pandas as pd
from bs4 import BeautifulSoup
import requests

def crawl_ifrs(s_code):
    ent = list(s_code)[0][1].split(".")[0]
    ent = str(ent)
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A"+ent+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=701"
    table_list = pd.read_html(url, encoding='UTF-8')

    ifrs = table_list[10]

    ifrs = ifrs.fillna('9999999999')
    for i in range(1, 5):
        if ifrs.iloc[:, i].dtype == 'O':
            ifrs.iloc[:, i] = ifrs.iloc[:, i].apply(lambda x: '9999999999' if type(x) == str else x)
            print(ifrs.iloc[:, i])
            ifrs.iloc[:, i] = ifrs.iloc[:, i].astype('float')
        ifrs.iloc[:, i] = ifrs.iloc[:, i].apply(lambda x: format(float(x), ','))

    ifrs = pd.concat([ifrs.iloc[:, 0], ifrs['Annual']], axis=1)
    ifrs = ifrs.astype(str)

    for i in range(1, 5):
        ifrs.iloc[:12, i] = ifrs.iloc[:12, i].apply(lambda x: x[:-2])
        ifrs.iloc[18:21, i] = ifrs.iloc[18:21, i].apply(lambda x: x[:-2])
        ifrs.iloc[23:24, i] = ifrs.iloc[23:24, i].apply(lambda x: x[:-2])
    ifrs = ifrs.replace(['9,999,999,999', '9,999,999,999.0'], ['-', '-'])

    ifrs.rename(columns={'IFRS(연결)': ''}, inplace=True)
    ifrs = ifrs.to_html(justify="right", index=False, classes="table table-hover table-responsive bg-transparent")
    ifrs = ifrs.replace('border="1"', 'border="0"')
    pd.options.display.float_format = '{:,.0f}'.format
    ifrs = ifrs.replace('<td>', '<td align="right">')
    ifrs = ifrs.replace('<th>', '<th style="text-align: right;">')
    ifrs = ifrs.replace('halign="left"', 'style="text-align: center;"')
    ifrs = ifrs.replace('class ="table table-hover table-responsive bg-transparent"',
                        'class ="table table-hover table-responsive bg-transparent"')

    return (ifrs)

def tujaja(stock_code):
    ent = list(stock_code)[0][1].split(".")[0]
    gcode = str(ent)
    #gcode = str(stock_code)

    url = "https://finance.naver.com/item/frgn.naver?code="+gcode
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    req = requests.get(url, headers=headers)
    html = BeautifulSoup(req.text, "html.parser")
    html_table = html.select("table")

    table = pd.read_html(str(html_table), encoding='utf-8',  thousands=None, converters={'Account': str})

    table = table[2]
    data = table.dropna()

    data = data.values.tolist()

    return data

def summary(stock_code):
    ent = list(stock_code)[0][1].split(".")[0]
    gcode = str(ent)
    URL = "https://finance.naver.com/item/main.nhn?code=" + gcode
    response = requests.get(URL)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    summary_info = []  # 기업개요
    summary_p = soup.select('#summary_info p')
    for p in summary_p:
        summary_info.append(p.text)

    return summary_info

def invest_opinion(stock_code):
    ent = list(stock_code)[0][1].split(".")[0]
    gcode = str(ent)
    url = 'https://comp.fnguide.com/SVO2/json/data/01_06/03_A' + gcode + '.json'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    ab = str(soup)
    bc = ab.split('}')
    name = []
    date = []
    target_prc = []
    target_prc_bf = []
    yoy = []
    recom_cd = []
    recom_cd_bf = []
    avg = []

    if bc[0]:
        try:
            name.append(bc[0].split('"')[9])
            date.append(bc[0].split('"')[13])
            target_prc.append(bc[0].split('"')[17])
            target_prc_bf.append(bc[0].split('"')[21])
            yoy.append(bc[0].split('"')[25])
            recom_cd.append(bc[0].split('"')[29])
            recom_cd_bf.append(bc[0].split('"')[33])
        except:
            None

    i = 1
    for items in bc:
        try:
            if bc[i]:
                name.append(bc[i].split('"')[7])
                date.append(bc[i].split('"')[11])
                target_prc.append(bc[i].split('"')[15])
                target_prc_bf.append(bc[i].split('"')[19])
                yoy.append(bc[i].split('"')[23])
                recom_cd.append(bc[i].split('"')[27])
                recom_cd_bf.append(bc[i].split('"')[31])
                i += 1
            else:
                break
        except:
            break

    recom = bc[0].split('"')[37]
    recom_bf = bc[0].split('"')[41]
    avg.append(recom)
    avg.append(recom_bf)
    recom_float = float(recom.replace(",", ""))
    recom_bf_float = float(recom_bf.replace(",", ""))
    avg_num = round(((recom_float - recom_bf_float) / recom_bf_float * 100), 2)
    avg.append(avg_num)
    avg.append(bc[0].split('"')[45])
    avg.append(bc[0].split('"')[49])


    return name, date, target_prc, target_prc_bf, yoy, recom_cd, recom_cd_bf, avg

