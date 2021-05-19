# encoding=utf-8
"""
Editor : Yusang Jeon

라이엇 API를 활용한 천상계 데이터 수집

"""

import pandas as pd
import requests
import urllib

url_base = 'https://kr.api.riotgames.com'

def get_api_key():
    """
    api key : 2021-05-17
    """
    f = open("mod/lol_api_key.txt", 'r')
    # f = open("mini_project/lol_api_key.txt", 'r')
    api_key = f.readline()
    f.close()

    return api_key

def make_url_league(league, api_key, tier=0):
    """
    솔랭 리그별 플레이어 리스트 불러오는 url 만들기
    """

    league_list = ['grandmaster', 'master', 'diamond', 'platinum']
    tier_list = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
    query = {}

    if league in league_list:
        if league == 'grandmaster':
            url_league = '/grandmasterleagues/by-queue/RANKED_SOLO_5x5'
        elif league == 'master':
            url_league = '/masterleagues/by-queue/RANKED_SOLO_5x5'
        else:
            url_league = f'/entries/RANKED_SOLO_5x5/{league.upper()}/{tier_list[tier]}'
            query['page'] = 1   # 일단 1페이지만 포함
    else:
        raise ValueError

    query['api_key'] = api_key
    option = urllib.parse.urlencode(query)

    # 리그별 소환사 목록 불러오기
    url = url_base + '/lol/league/v4' + url_league + f'?{option}'

    return url

def make_url_summoner(id, api_key):

    query = {}
    query['api_key'] = api_key
    option = urllib.parse.urlencode(query)

    url = url_base + f'/lol/summoner/v4/summoners/{id}' + f'?{option}'

    return url

def make_url_matches():
    pass


# request
def get_league_df(url):

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Response code is not 200")

    temp = response.text
    temp = temp.replace('true', 'True')
    temp = temp.replace('false', 'False')

    data_dict = eval(temp)

    df = pd.DataFrame(data_dict['entries'])
    # print(df.columns)
    # print(df['veteran'].head())

    return df

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

# ----------------------------

if __name__ == '__main__':
    api_key = get_api_key()
    url_league = make_url_league(league='grandmaster', api_key=api_key)
    df_league = get_league_df(url_league)

    print(df_league.columns)
    # print(df.loc[0])

    df_summoners = pd.DataFrame()
    for summoner_id in df_league['summonerId']:
        url_summoner = make_url_summoner(id=summoner_id, api_key=api_key)
        temp_df = get_summoner_df(url_summoner)

        # df_summoners.loc[len(df_summoners)] = temp_df     # wrong code
        df_summoners = pd.concat([df_summoners, temp_df])

    print(df_summoners)

