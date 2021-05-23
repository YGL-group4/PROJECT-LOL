# coding=utf-8
"""
-----------------------------------------------------------------------------------
메인 함수

# Description:
1.
2.
3.
4.
5.

-----------------------------------------------------------------------------------
"""

from MiniProject1.src.config import folder
from MiniProject1.src.data_process import summoners
from MiniProject1.src.data_process import crawling
from MiniProject1.src.model import modeling

import pandas as pd


class MainFunction():

    def __init__(self):
        self.data = None
        self.model = None
        self.score = None

    # 1. make data
    def make_data(self):
        """
        학습할 데이터를 생성한다.
        """
        ################## fill in the code  ###################
        # df_summoners = summoners.get_summoners_list()
        # df_data = crawling.get_data(df_summoners)

        # df_data.to_csv('data_name.csv')
        ########################################################

    # 2. get data
    def get_data(self):
        """
        data를 가져옴
        :return: loaded data
        """
        path = folder.get_data_path('challenger_0521.csv')
        data = pd.read_csv(path, index_col=0)

        return data

    # 3. create and train model
    def train_model(self):
        ################## fill in the code  ###################

        # self.model = ???

        ########################################################
        pass

    # 4. test model
    def test_model(self):
        ################## fill in the code  ###################

        # print result

        ########################################################
        pass

    # 5. evaluate model
    def evaluate_model(self):
        ################## fill in the code  ###################

        # print result

        ########################################################
        pass


if __name__ == '__main__':

    func = MainFunction()
    func.get_data()
    func.train_model()
    func.test_model()
    func.evaluate_model()