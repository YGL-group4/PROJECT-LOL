# encoding=utf-8
"""
Editor : Yusang Jeon
Date : 2021-05-20

미드라인 승패 예측 모델 만들기
"""


from tensorflow import keras
import pandas as pd
import numpy as np

# 랜덤 시드 고정
np.random.seed(5)

# 1. get dataset ( position = mid )
df = pd.read_csv('challenger_log_rev.csv')
df = df[df['position'] == 'mid']
df = df.drop('position', axis=1)

# mm:ss -> second
def to_second(time_str):
    m = int(time_str[:2])
    s = int(time_str[3:])
    return m * 60 + s
df_temp = df['play time'].copy()
df_temp = df_temp.apply(to_second)
df['play time'] = df_temp

dataset = df.values # (1073, 11)

# 2. split dataset
x_train = dataset[:900, 1:]
y_train = dataset[:900, 0]
x_test = dataset[900:, 1:]
y_test = dataset[900:, 0]

# 3. model design
model = keras.Sequential()
model.add(keras.layers.Dense(8, input_dim=11, activation='relu'))
model.add(keras.layers.Dense(8, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))

# 4. model compile setting
# model.compile(optimizer='sgd', loss='mse')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 5. train model
model.fit(x_train, y_train, epochs=100, batch_size=64)

# 6. Evalutation
scores = model.evaluate(x_test, y_test)
# print(f"{model.metrices_name[1]}: {scores[1]*100}")
# print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
print(model.metrics_names)
print(scores)

