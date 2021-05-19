# encoding=utf-8
"""
Editor : Yusang Jeon

Blitz
주어진 소환사의 라인별 전적검색, 지표 가져오기

예시 링크 : 팀개못하면누누함
https://poro.gg/summoner/kr/%ED%8C%80%EA%B0%9C%EB%AA%BB%ED%95%98%EB%A9%B4%EB%88%84%EB%88%84%ED%95%A8

"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import time
import os

url_base = 'https://poro.gg/summoner/kr/'

def crawling(df):
    """
    소환사명 명단을 받은 뒤, 최근 전적검색 데이터 크롤링
    :param df: 소환사명 명단 ('summonerName')
    :return: 포지션별 지표 및 승률
    """
    dir = os.path.dirname(__file__)
    path_driver = os.path.join(dir, 'chromedriver.exe')

    driver = webdriver.Chrome(path_driver)
    data = pd.DataFrame()
    for name in df['summonerName']:
        df_temp = get_user_log(name, driver=driver)
        if type(df_temp) == type(-1):
            continue
        else:
            data = pd.concat([data, df_temp])

    driver.close()

    # print(data)

    return data

def get_user_log(name, driver=None):
    """
    드라이버가 열린상태에서, 해당 소환사명을 poro.gg 에서 검색
    이후 최근 전적 데이터 크롤링
    :param name: 소환사명
    :param driver: 열려있는 webdriver
    :return: 데이터프레임(포지션별 KDA, ..., 승률) 반환, 소환사명 없으면 -1 반환
    """

    def find_position(game, name):
        """
        현재 게임에서 포지션이 어디인지 찾아조는 함수
        :param game: 현재 게임의 정보를 담은 html 태그
        :return: 포지션명(top, jug, mid, adc, sup)
        """
        position = 'None' # default
        position_list = ['top', 'jug', 'mid', 'adc', 'sup']
        players = game.select('div > div.summoners > div.summoner')[:10]
        for n, player in enumerate(players):
            if name in str(player):
                position = position_list[n % 5]

        return position

    if driver == None:
        raise ValueError("driver is not open!!")
    # html 파싱하기
    url = make_url(name)
    driver.get(url)
    print(f"소환사명 : {name}", end='')
    time.sleep(3)

    # 소환사명 없는 경우 예외처리
    try:
        driver.find_element_by_id('search-not-found')
    except:
        print()
    else:
        print(" (not found)")
        return -1

    driver.find_elements_by_css_selector('div > button.match-history-filter__queue-type')[1].click()
    time.sleep(3)

    html = driver.page_source
    html_ps = BeautifulSoup(html, 'lxml')

    games = html_ps.select('div > div.match-history-container > div.mt-2 > div.match-history')

    df = pd.DataFrame()
    win = {'승리': 1, '패배': 0}
    for game in games:
        temp_df = {}

        text_win = game.select('div > div.match-history__result')[0].text
        if text_win not in win:
            continue # 다시하기는 패스
        temp_df['win'] = win[text_win]
        temp_df['position'] = find_position(game, name)
        temp_df['play time'] = game.select('div > span.mt-md-1')[0].text

        kda = game.select('div > div.kda > span')
        temp_df['kill'] = int(kda[0].text)
        temp_df['death'] = int(kda[1].text)
        temp_df['assist'] = int(kda[2].text)
        # temp_df['kda'] = (int(kda[0].text) + int(kda[2].text)) / int(kda[1].text)

        info = game.select('div.info > span')
        temp_df['kill participation(%)'] = int(info[0].text[:-1])
        temp_df['cs'] = int(info[1].text)
        temp_df['vision score'] = int(info[3].text)

        wards = game.select('div.wards.mt-1 > div')
        temp_df['pink ward'] = int(wards[0].text)
        temp_df['ward'] = int(wards[1].text)
        temp_df['break ward'] = int(wards[2].text)

        temp_df = pd.DataFrame([temp_df])

        df = pd.concat([df, temp_df])


    return df

def make_url(name):
    name = urllib.parse.quote(name)
    url = url_base + name

    return url

# ----------test code

def test():
    df = pd.DataFrame(['팀개못하면누누함'])
    df.columns = ['summonerName']

    result = crawling(df)

    print(result)


if __name__ == '__main__':
    challenger_list = pd.read_csv('challenger_list.csv')

    top10 = challenger_list.loc[:10]
    data = crawling(top10)

    data.to_csv('top10_line_data.csv')
