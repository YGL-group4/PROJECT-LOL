# encoding=utf-8
"""
메인 파일
"""
# from mod import *

from mod import riotkey
api_key = riotkey.get_api_key()

from mod import lol_api
df_challenger = lol_api.get_challenger_df()
df_grandmaster = lol_api.get_grandmaster_df()

from mod import crawling_poro

data_challenger = crawling_poro.crawling(df_challenger)
data_grandmaster = crawling_poro.crawling(df_grandmaster)

data_challenger.to_csv('challenger_log.csv')
data_grandmaster.to_csv('grandmaster_log.csv')

