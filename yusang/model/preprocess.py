# encoding=utf-8

import pandas as pd

def split_data(df_x, df_y, test_size=0.2):
    """
    모델의 input data와 output data를 train, test로 분할해주는 함수
    :param df_x: input data
    :param df_y: output data
    :param test_size: test data의 비율
    :return: train(input, output), test(input, output) -> 총 4개
    """
    if len(df_x) != len(df_y):
        raise ValueError("input과 output의 길이가 다릅니다.")

    idx_split = int(len(df_x) * (1 - test_size))

    x_train = df_x.loc[:idx_split]
    x_test = df_x.loc[idx_split:]
    y_train = df_y.loc[:idx_split]
    y_test = df_y.loc[idx_split:]

    return x_train, y_train, x_test, y_test

