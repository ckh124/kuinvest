import requests
from bs4 import BeautifulSoup


def priceindex():
    response = requests.get("https://finance.naver.com/sise/")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    Kospi_chart = soup.find('div', id='tab_sel1_sise_main_chart')
    Kosdaq_chart = soup.find('div', id='tab_sel2_sise_main_chart')
    Kospi_chart_url = Kospi_chart.find('img')['src']  # 코스피 차트 img url
    Kosdaq_chart_url = Kosdaq_chart.find('img')['src']  # 코스닥 차트 img url
    ul = soup.select('ul.tab_sel1')[0]
    Scham = [item.get_text().strip() for item in ul.select('span.num')][:2]  # 코스피,코스닥 수치
    Fluctuation = [item.get_text().strip() for item in ul.select('span.num_s')][:2]  # 코스피,코스닥 등락률,수치
    Kospi_scham = Scham[0]  # 코스피 수치
    Kosdaq_scham = Scham[1]  # 코스닥 수치
    Kospi_f = Fluctuation[0].split()  # 코스피 등락률
    Kospi_f[1] = Kospi_f[1][0:6]
    Kosdaq_f = Fluctuation[1].split()  # 코스닥 등락률
    Kosdaq_f[1] = Kosdaq_f[1][0:6]
    Kospi_trend = soup.select('ul#tab_sel1_deal_trend')[0]
    Kosdaq_trend = soup.select('ul#tab_sel2_deal_trend')[0]
    Kospi_trading = [item.get_text().strip() for item in Kospi_trend.select('li')][1:]  # 코스피 투자자별 매매동향
    Kosdaq_trading = [item.get_text().strip() for item in Kosdaq_trend.select('li')][1:]  # 코스닥 투자자별 매매동향
    return Kospi_chart_url, Kosdaq_chart_url, Kospi_scham, Kosdaq_scham, Kospi_f, Kosdaq_f, Kospi_trading, Kosdaq_trading



