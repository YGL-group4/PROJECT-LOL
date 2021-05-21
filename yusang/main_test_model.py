from model import preprocess
from model import modeling
from setting import folder
import pandas as pd
import sys

# 출력결과 로그를 stdout.txt에 저장 시작
path_log = folder.get_data_path('model test log.txt')
sys.stdout = open(path_log, 'w', encoding="UTF-8")

# 챌린저 게임 데이터 가져오기
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
x_train, scaler = preprocess.scale_data(x_train)
lr = modeling.LR_model(x_train, y_train)
score_train = lr.score(x_train, y_train)
print(f"train score : {score_train}")

# test model
print("x_test", x_test.shape)
x_test, scaler = preprocess.scale_data(x_test, scaler=scaler)
score_test = lr.score(x_test, y_test)
print(f"test score : {score_test}")

# --------------------------------------------
# 다른 데이터도 넣고 테스트해보기
from module import lol_api
from module import crawling

print("="*30)
my_df = lol_api.get_summoner_df('김치유상균')
my_data = crawling.get_data(my_df)
print("********load my data!")

my_data = my_data[my_data['position'] == 'mid']
my_data = my_data.drop(['position'], axis=1)

x, y = preprocess.input_output(my_data)
x, scaler = preprocess.scale_data(x, scaler=scaler)
my_score = lr.score(x, y)
print('내 전적으로 점수내기 ->', my_score)
y_pred = lr.model.predict(x)
print("예측", y_pred)
print("실제", y.to_numpy())
print("-> ", y_pred == y.to_numpy())

# 출력결과 로그에 저장 완료
sys.stdout.close()
