from model import preprocess
from model import log_reg
from setting import folder
import pandas as pd

# 문자열로 저장된 플레이타임을 위한 함수
def time_to_second(time_str):
    second = int(time_str[:2]) * 60 + int(time_str[3:])
    return second

path_df = folder.get_data_path('challenger_log_rev.csv')
df = pd.read_csv(path_df, index_col=0)

# 플레이타임 초 단위 int형으로 바꾸기
df_temp = df['play time'].copy()
df_temp = df_temp.apply(time_to_second)
df['play time'] = df_temp

# 20분 이상 데이터만 남김
df = df[df['play time'] >= 1200]

# input, output 분리
col_x = list(df.columns)
col_y = 'win'
col_x.remove(col_y)

x = df[col_x]
y = df[col_y]

# train, test 분리
x_train, y_train, x_test, y_test = preprocess.split_data(x, y)

# train model

# test model

# print score, accuracy