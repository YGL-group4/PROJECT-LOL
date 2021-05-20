# encoding=utf-8
"""
Editor : Yusang Jeon

라이엇 API를 활용한 천상계 데이터 수집

** /data에 lol_api_key.txt가 있어야함. **

"""

import pandas as pd
import requests
import urllib
from yusang.setting import folder

url_base = 'https://kr.api.riotgames.com'

def get_api_key():
    """
    라이엇 API 인증키를 저장된 lol_api_key.txt로부터 불러오는 함수
    """
    path_key = folder.get_data_path('../data/lol_api_key.txt')

    f = open(path_key, 'r')
    api_key = f.readline()
    f.close()

    return api_key

def get_summoners(league, tier=0):
    """
    주어진 리그에 속한 소환사들의 명단을 만드는 함수
    :param league: 리그명(challenger, grandmaster, master, diamond, platinum)
    :param tier: 티어(다이아, 플레 리그만 값을 받으며, 1~4의 정수)
    :return: 해당 리그의 소환사들 명단을 담은 Dataframe
    """
    def make_url_league(league, tier=0):
        """
        솔랭 리그별 플레이어 리스트 불러오는 url 만들기
        """
        league_list = ['challenger', 'grandmaster', 'master', 'diamond', 'platinum']
        tier_list = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
        query = {}

        if league in league_list:
            if league == 'challenger':
                print("챌린저 리그를 불러옵니다...")
                url_league = '/challengerleagues/by-queue/RANKED_SOLO_5x5'
            elif league == 'grandmaster':
                print("그랜드마스터 리그를 불러옵니다...")
                url_league = '/grandmasterleagues/by-queue/RANKED_SOLO_5x5'
            elif league == 'master':
                print("마스터 리그를 불러옵니다...")
                url_league = '/masterleagues/by-queue/RANKED_SOLO_5x5'
            else:
                print("플레 or 다이아 리그를 불러옵니다...")
                url_league = f'/entries/RANKED_SOLO_5x5/{league.upper()}/{tier_list[tier]}'
                query['page'] = 1  # 일단 1페이지만 포함
        else:
            raise ValueError

        query['api_key'] = get_api_key()
        option = urllib.parse.urlencode(query)

        # 리그별 소환사 목록 불러오기
        url = url_base + '/lol/league/v4' + url_league + f'?{option}'

        return url

    url = make_url_league(league, tier=tier)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Response code is not 200, please check Riot API key")

    temp = response.text
    temp = temp.replace('true', 'True')
    temp = temp.replace('false', 'False')

    data_dict = eval(temp)

    df = pd.DataFrame(data_dict['entries'])

    return df

def get_grandmaster_df():
    """
    그랜드마스터 리그의 소환사명 명단을 찾아오는 함수
    :return: 그랜드마스터 소환사명이 나열된 Dataframe
    """
    df_league = get_summoners(league='grandmaster')

    # 랭크 점수 순서대로, 소환사명을 나열
    df = df_league[['summonerName', 'leaguePoints']]
    df = df.sort_values('leaguePoints', ascending=False)
    df = df.reset_index(drop=True)

    return df

def get_challenger_df():
    """
    챌린저 리그의 소환사명 명단을 찾아오는 함수
    :return: 챌린저 소환사명이 나열된 Dataframe
    """
    df_league = get_summoners(league='challenger')

    # 랭크 점수 순서대로, 소환사명을 나열
    df = df_league[['summonerName', 'leaguePoints']]
    df = df.sort_values('leaguePoints', ascending=False)
    df = df.reset_index(drop=True)

    return df


# ---------------------------- 이하 테스트코드

def make_url_matches():
    pass


def make_url_summoner(id, api_key):

    query = {}
    query['api_key'] = api_key
    option = urllib.parse.urlencode(query)

    url = url_base + f'/lol/summoner/v4/summoners/{id}' + f'?{option}'

    return url

def get_summoner_df(url):

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Response code is not 200")

    data_dict = eval(response.text)
    df = pd.DataFrame([data_dict])

    # column 순서 변경
    col1 = ["name"]
    col2 = df.columns.to_list()
    col2.remove("name")
    df = df[col1 + col2]

    print(df.columns)

    return df


if __name__ == '__main__':

    df = get_challenger_df()
    print(df.head())

    # df.to_csv('challenger_list.csv')


