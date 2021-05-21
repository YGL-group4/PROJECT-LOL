# encoding=utf-8

from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def input_output(df):
    """
    'win'을 target으로 하도록 input, output 분리
    :param df: 전체 Dataframe
    :return: input(feature) Dataframe, output(target) Dataframe
    """
    col_x = list(df.columns)
    col_y = 'win'
    col_x.remove(col_y)

    x = df[col_x]
    y = df[col_y]

    return x, y


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

    x_train = df_x.iloc[:idx_split]
    x_test = df_x.iloc[idx_split:]
    y_train = df_y.iloc[:idx_split]
    y_test = df_y.iloc[idx_split:]

    return x_train, y_train, x_test, y_test

def longer_playtime(df, time_str: str):
    """
    df의 play time이 time_str(e.g. 20:00)보다 긴 data만 반환
    :param df: 게임 전적이 담긴 Dataframe
    :param time_str: mm:ss 형식의 시간
    :return: time_str 이후의 플레이타임을 가진 것만 Dataframe으로 반환
    """
    second = time_str.split(':')
    second = int(second[-2]) * 60 + int(second[-1])
    df_result = df[df['play time'] >= second]

    return df_result

# Scaling
def scale_data(x):
    """
    sklearn의 MinMaxScaler를 활용한다.
    input data를 scaling한다.
    :param x_train: input data for train
    :param y_train: output data for train
    :return: scaled input, output data for train
    """
    scaler = MinMaxScaler()

    scaled_x = scaler.fit_transform(x)
    # scaled_x = scaler.transform(x)

    return scaled_x