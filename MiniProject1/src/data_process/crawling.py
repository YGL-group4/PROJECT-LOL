# coding=utf-8
"""
-----------------------------------------------------------------------------------
# Description:
1. summoners.py에서 소환사 명단을 가져온다.
2. 가져온 소환사 명단을 토대로 최근 전적을 크롤링한다.
3. 데이터를 반환한다 / 저장한다.

-----------------------------------------------------------------------------------
# Reference: poro.gg
"""

from MiniProject1.src.config import folder

from selenium import webdriver
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import time


# 크롤링할 전적 사이트 : poro.gg
class PoroCrawling():

    def __init__(self):
        pass


# 크롤링할 전적 사이트 : poro.gg
# Editor : Yusang Jeon
class PoroCrawling1():
    """
    poro.gg에서 전적 데이터를 크롤링합니다.
    """
    url_base = 'https://poro.gg/summoner/kr/'

    def __init__(self, df_summoners):
        self.data = None
        self.get_data(df_summoners)
        # self.save_data(self.data, 'csv file name.csv')

    def save_data(self, data, file_name: str):
        """
        크롤링한 데이터를 data 폴더에 저장하는 함수
        :param data: 크롤링한 데이터를 담은 Dataframe
        :param file_name: 저장할 csv 파일명
        """
        path_data = folder.get_data_path(file_name)
        data.to_csv(path_data)

    def get_data(self, df_summoners):
        path_driver = chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(path_driver)
        driver.implicitly_wait(3)

        num_summoner = len(df_summoners['summonerName'])

        print(f"{num_summoner}명의 소환사 정보를 불러옵니다...")

        data = pd.DataFrame()
        num_success = 0
        num_fail = 0
        for name in df_summoners['summonerName']:
            print(f'({num_success + num_fail + 1}/{num_summoner}) ', end='')

            df_temp = self.get_user_log(name, driver=driver)
            if type(df_temp) == type(-1):
                num_fail += 1
                continue
            else:
                num_success += 1
                data = pd.concat([data, df_temp])

        driver.close()
        print(f"크롤링 완료! (성공:{num_success}, 실패:{num_fail})")

        self.data = data

    def get_user_log(self, name, driver=None):
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
            position = 'None'  # default
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
        url = self.make_url(name)
        driver.get(url)
        print(f"소환사 <{name}> 정보 로딩 중...", end='')
        time.sleep(2.5)
        # 소환사명 없는 경우 예외처리
        try:
            driver.find_element_by_id('search-not-found')
        except:
            print(" (success)", end='')
        else:
            print(" (fail)")
            return -1  # 소환사명 검색 실패

        # 솔로 랭크 클릭
        driver.find_elements_by_css_selector('div > button.match-history-filter__queue-type')[1].click()
        time.sleep(2)

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
                continue  # 다시하기는 패스

            temp_df['position'] = find_position(game, name)
            playtime_str = game.select('div > span.mt-md-1')[0].text
            playtime_str = playtime_str.split(':')
            temp_df['play time'] = int(playtime_str[-2]) * 60 + int(playtime_str[-1])

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

    def make_url(self, name):
        name = urllib.parse.quote(name)
        url = self.url_base + name

        return url



# 크롤링할 전적 사이트 : op.gg
class OpggCrawling():

    def __init__(self):
        pass