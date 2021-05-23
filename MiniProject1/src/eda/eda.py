"""
# -*- coding: utf-8 -*-
-----------------------------------------------------------------------------------
# Description:
정확한 데이터 분석을 위해서 데이터에 대한 이해를 선행함

# Author: Sunwung Lee
# DoC: 2021.05.23
-----------------------------------------------------------------------------------
"""
from matplotlib import font_manager, rc
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import platform
from IPython.display import display

import warnings
warnings.filterwarnings('ignore')

matplotlib.rcParams['axes.unicode_minus'] = False

class Eda:
    def __init__(self):
        print("class Eda")
    #
    # 각 라인별 최상위권 플레이어의 데이터가 가진 정보를 파악
    #
    def read_data_from_excel(self, _filepath, _filename):
        import_file = _filepath + _filename
        self.df_top = pd.read_excel(import_file, sheet_name="탑")
        self.df_jug = pd.read_excel(import_file, sheet_name="정글")
        self.df_mid = pd.read_excel(import_file, sheet_name="미드")
        self.df_adc = pd.read_excel(import_file, sheet_name="원딜")
        self.df_sup = pd.read_excel(import_file, sheet_name="서포터")
        # print(df_sup)
        print(f'탑 데이터 크기: {self.df_top.shape}')
        print(f'정글 데이터 크기: {self.df_jug.shape}')
        print(f'미드 데이터 크기: {self.df_mid.shape}')
        print(f'원딜 데이터 크기: {self.df_adc.shape}')
        print(f'서포터 데이터 크기: {self.df_sup.shape}')
        print()

        print("TOP 데이터 상단 5개 출력")
        display(self.df_top.head())

        print("TOP 데이터의 기초 통계량 확인")
        display(self.df_top.describe())

    def time_to_sec(self, time):
        minutes = int(time.split(':')[0])
        secs = int(time.split(':')[1])
        return (minutes*60 + secs)

    def choose_role(self, role):
        if role == '탑':
            role_en = "TOP"
            df = self.df_top
        elif role == '정글':
            role_en = "JUNGLE"
            df = self.df_jug
        elif role == '미드':
            role_en = "MIDDLE"
            df = self.df_mid
        elif role == '원딜':
            role_en = "AD CARRY"
            df = self.df_adc
        elif role == '서포터':
            role_en = "SUPPORTER"
            df = self.df_sup
        elif role == '전체':
            role_en = "TOTAL"
            df = pd.concat([self.df_top, self.df_jug, self.df_mid,
                            self.df_adc, self.df_sup])
        else:
            print("에러")
        self.role_en = role_en
        self.df = df

if __name__ == '__main__':
    filepath = '../../dataset/'
    filename = '2021-5-20_top_1_to_100_by_role.xlsx'



    role = str(input("확인하고싶은 라인을 입력:"))
    print()
    print(f"{role}에 관련된 데이터를 가져옵니다.")
