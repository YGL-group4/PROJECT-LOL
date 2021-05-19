# encoding=utf-8
"""
Editor : Yusang Jeon

Blitz
주어진 소환사의 라인별 전적검색, 지표 가져오기

예시 링크 : Hide on bush
https://blitz.gg/lol/profile/kr/hide%20on%20bush/champions?role=SPE&queue=all&patch=all&class=all

"""

import requests
import urllib
import pandas as pd

url_crw = 'https://blitz.gg/lol/profile/kr'

def get_user_log(name):

    url_top = make_url(name, "TOP")
    url_jug = make_url(name, "JUNGLE")
    url_mid = make_url(name, "MID")
    url_adc = make_url(name, "ADC")
    url_sup = make_url(name, "SUPPORT")



    return df

def make_url(name, position):

    # role = SPE(ALL), TOP, JUNGGLE, MID, ADC, SUPPORT
    query = {
        "queue": 420,
        "roll": position,
        "patch": "all",
        "class": "all"
    }

    option = urllib.parse.urlencode(query)
    name = urllib.parse.quote(name)

    url = url_crw + f'/{name}/champions' + f'?{option}'

    return url

