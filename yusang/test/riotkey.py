# encoding=utf-8
"""
Editor : Yusang Jeon

같은 디렉토리 내의 "lol_api_key.txt"에 적힌
라이엇 API 인증키를 불러오는 모듈

인증키 있는 주소 : https://developer.riotgames.com/

"""

url_base = 'https://kr.api.riotgames.com'

def get_api_key():
    """
    api key : 2021-05-18
    """
    f = open("../mod/lol_api_key.txt", 'r')
    api_key = f.readline()
    f.close()

    return api_key