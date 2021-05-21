# encoding=utf-8

from sklearn.linear_model import LogisticRegression
import pandas as pd

# 모델 생성
class LR_model():

    def __init__(self, x_train, y_train):
        model = LogisticRegression()
        model.fit(x_train, y_train)
        self.model = model

    def score(self, x, y):
        return self.model.score(x, y)



# logistic regression 적용
# 학습
# 예측하기
