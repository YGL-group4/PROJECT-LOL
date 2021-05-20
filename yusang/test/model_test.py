from tensorflow import keras
import pandas as pd

dnn = keras.Sequential()
dnn.add(keras.layers.Dense(units=1, input_shape=(1,)))
dnn.compile(optimizer='sgd', loss='mse')

# dataset 불러오기
df = pd.read_csv('yusang/challenger_log.csv')


dnn.fit()
