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

    news = dict(zip(news_title, news_link))

    return news