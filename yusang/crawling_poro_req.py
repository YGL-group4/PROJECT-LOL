# encoding=utf-8
"""
Editor : Yusang Jeon

Blitz
주어진 소환사의 라인별 전적검색, 지표 가져오기

예시 링크 : 팀개못하면누누함
https://poro.gg/summoner/kr/%ED%8C%80%EA%B0%9C%EB%AA%BB%ED%95%98%EB%A9%B4%EB%88%84%EB%88%84%ED%95%A8

"""

import requests
import urllib
import pandas as pd
from bs4 import BeautifulSoup

url_base = 'https://poro.gg/summoner/kr/'

def get_user_log(name):

    df = pd.DataFrame()
    # df['position'] = top, jug, mid, adc, sup

    return df

def make_url(name):
    name = urllib.parse.quote(name)
    url = url_base + name

    return url

# ----------test code

name = "팀개못하면누누함"
name = urllib.parse.quote(name)
url = url_base + name
response = requests.get(url)
html = response.text
html_ps = BeautifulSoup(html, 'lxml')

# temp = html_ps.find("div", {"class": "match-history-container mt-3"})
temp = html_ps.select("div.mt-2")
