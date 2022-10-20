import requests
from bs4 import BeautifulSoup


def newscrawling():
    req = requests.get('https://finance.naver.com/news/news_list.naver?mode=RANK')
    soup = BeautifulSoup(req.text, 'html.parser')
    hotnews = soup.find('ul', class_='newsList')

    news_link = []
    news_title = []

    for href in hotnews.find_all("li"):
        news_link.append('finance.naver.com' + (href.find("a")["href"]))

    rem = []
    for items in news_link:
        if items not in rem:
            rem.append(items)
    news_link = rem

    for title in hotnews.find_all("li"):
        news_title.append(title.find("a")["title"])

    rem = []
    for items in news_title:
        if items not in rem:
            rem.append(items)
    news_title = rem

    news_link = news_link[:-3]
    news_title = news_title[:-3]

    news = dict(zip(news_title, news_link))

    return news

def stock_news(stock_code):
    gcode = list(stock_code)[0][1].split(".")[0]
    url = 'https://finance.naver.com'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    req = requests.get(url+'/item/news.naver?code='+gcode, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    iframe = soup.find('iframe', id='news_frame')

    nurl = url+iframe['src']
    req1 = requests.get(nurl)
    soup2 = BeautifulSoup(req1.content, 'html.parser')
    snews = soup2.findAll('td', {'class': 'title'})

    news_link = []
    news_title = []

    for href in snews:
        news_link.append(url + (href.find("a")["href"]))

    rem = []
    for items in news_link:
        if items not in rem:
            rem.append(items)
    news_link = rem

    for title in snews:
        news_title.append(title.find("a").get_text())

    rem = []
    for items in news_title:
        if items not in rem:
            rem.append(items)
    news_title = rem

    news = dict(zip(news_title, news_link))

    return news