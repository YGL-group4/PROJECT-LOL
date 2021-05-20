# encoding=utf-8
"""
Editor : Yusang Jeon

poro.gg에서 소환사의 라인별 전적검색, 지표 가져오기

예시 링크 : 팀개못하면누누함
https://poro.gg/summoner/kr/%ED%8C%80%EA%B0%9C%EB%AA%BB%ED%95%98%EB%A9%B4%EB%88%84%EB%88%84%ED%95%A8

"""

from selenium import webdriver
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import time
from yusang.setting import folder


url_base = 'https://poro.gg/summoner/kr/'

def get_data(df):
    """
    소환사명 명단을 받은 뒤, 최근 전적검색 데이터 크롤링
    :param df: 소환사명 명단 ('summonerName')
    :return: 포지션별 지표 및 승률
    """

    path_driver = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path_driver)
    driver.implicitly_wait(3)

    print(f"{len(df['summonerName'])}명의 소환사 정보를 불러옵니다...")

    data = pd.DataFrame()
    num_success = 0
    num_fail = 0
    for name in df['summonerName']:
        df_temp = get_user_log(name, driver=driver)
        if type(df_temp) == type(-1):
            num_fail += 1
            continue
        else:
            num_success += 1
            data = pd.concat([data, df_temp])

    driver.close()
    print(f"소환사 정보 불러오기 완료! (성공:{num_success}, 실패:{num_fail}")

    return data

def get_user_log(name, driver=None):
    """드라이버가 열린상태에서, 다음과 같이 진행합니다.
    1. 해당 소환사명을 poro.gg 에서 검색
    2. 솔로랭크 항목 클릭
    3. 최근 전적 데이터 크롤링
    :param name: 소환사명
    :param driver: 열려있는 webdriver
    :return: 데이터프레임(포지션별 KDA, ..., 승률) 반환, 소환사명 없으면 -1 반환
    """

    def find_position(game, name):
        """
        현재 게임에서 포지션이 어디인지 찾아조는 함수
        :param game: 현재 게임의 정보를 담은 html 태그
        :param name: 소환사명
        :return: 포지션명(top, jug, mid, adc, sup)
        """
        position = 'None' # default
        position_list = ['top', 'jug', 'mid', 'adc', 'sup']
        players = game.select('div > div.summoners > div.summoner')[:10]
        for n, player in enumerate(players):
            if name in str(player):
                position = position_list[n % 5]

        return position

    def find_damage_rate(game, name):
        """
        현재 게임에서 팀 내 데미지 비중을 불러오는 함수
        :param game: 현재 게임의 정보를 담은 html 태그
        :param name: 소환사명
        :return: 소환사의 팀 내 데미지 비중(%)
        """
        pass

    # 드라이버 입력 안되었을 경우 오류 출력
    if driver == None:
        raise ValueError("driver is not open!!")

    # poro.gg에서 소환사명 검색
    url = make_url(name)
    driver.get(url)
    print(f"소환사 <{name}> 정보 로딩 중...", end='')
    time.sleep(3)
    # 소환사명 없는 경우 예외처리
    try:
        driver.find_element_by_id('search-not-found')
    except:
        print(" (success)", end='')
    else:
        print(" (fail)")
        return -1   # 소환사명 검색 실패

    # 솔로 랭크 클릭
    driver.find_elements_by_css_selector('div > button.match-history-filter__queue-type')[1].click()
    time.sleep(3)

    # html 파싱해오기
    html = driver.page_source
    html_ps = BeautifulSoup(html, 'lxml')

    # 최근 게임만 불러오기
    games = html_ps.select('div > div.match-history-container > div.mt-2 > div.match-history')
    print(f" --- {len(games)}판")

    df = pd.DataFrame()
    win = {'승리': 1, '패배': 0}
    for game in games:
        temp_df = {}

        text_win = game.select('div > div.match-history__result')[0].text
        if text_win not in win:
            continue # 다시하기는 패스

        temp_df['position'] = find_position(game, name)
        temp_df['play time'] = game.select('div > span.mt-md-1')[0].text

        kda = game.select('div > div.kda > span')
        temp_df['kill'] = int(kda[0].text)
        temp_df['death'] = int(kda[1].text)
        temp_df['assist'] = int(kda[2].text)
        # temp_df['kda'] = (int(kda[0].text) + int(kda[2].text)) / int(kda[1].text)

        info = game.select('div.info > span')
        temp_df['kill participation(%)'] = int(info[0].text[:-1])
        # temp_df['damage rate'] = find_damage_rate()
        temp_df['cs'] = int(info[1].text)
        temp_df['vision score'] = int(info[3].text)

        wards = game.select('div.wards.mt-1 > div')
        temp_df['pink ward'] = int(wards[0].text)
        temp_df['ward'] = int(wards[1].text)
        temp_df['break ward'] = int(wards[2].text)
        temp_df['win'] = win[text_win]

        temp_df = pd.DataFrame([temp_df])

        df = pd.concat([df, temp_df])


    return df

def make_url(name):
    name = urllib.parse.quote(name)
    url = url_base + name

    return url

def save_data(data, file_name: str):
    """
    크롤링한 데이터를 data 폴더에 저장하는 함수
    :param data: 크롤링한 데이터를 담은 Dataframe
    :param file_name: 저장할 csv 파일명
    """
    path_data = folder.get_data_path(file_name)
    data.to_csv(path_data)

# ----------practice code

def test():
    df = pd.DataFrame(['팀개못하면누누함'])
    df.columns = ['summonerName']

    result = get_data(df)

    print(result)


if __name__ == '__main__':
    challenger_list = pd.read_csv('challenger_list.csv')

    top10 = challenger_list.loc[:10]
    data = get_data(top10)

    data.to_csv('top10_line_data.csv')
