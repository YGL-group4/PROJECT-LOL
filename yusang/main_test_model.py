from model import preprocess
from model import modeling
from setting import folder
import pandas as pd

path_df = folder.get_data_path('challenger_0521.csv')
df = pd.read_csv(path_df, index_col=0)

# 20분 이상 데이터만 남김
df = preprocess.longer_playtime(df, "15:00")

# 미드부터 보자
df = df[df['position'] == 'mid']
df = df.drop(['position'], axis=1)

# input, output 분리
x, y = preprocess.input_output(df)
print("x, y :", x.shape, y.shape)

# train, test 분리
x_train, y_train, x_test, y_test = preprocess.split_data(x, y, test_size=0.3)

# train model
print("x_train", x_train.shape)
x_train = preprocess.scale_data(x_train)
lr = modeling.LR_model(x_train, y_train)
score_train = lr.score(x_train, y_train)
print(f"train score : {score_train}")

# test model
print("x_test", x_test.shape)
x_test = preprocess.scale_data(x_test)
score_test = lr.score(x_test, y_test)
print(f"test score : {score_test}")

