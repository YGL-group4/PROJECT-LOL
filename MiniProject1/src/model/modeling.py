# coding=utf-8
"""
-----------------------------------------------------------------------------------
# Class:
1. LogReg
2. NeuralNet
3. KNN


-----------------------------------------------------------------------------------
"""
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class LogReg():
    """
    Logistic Regression 모델 만들기
    """
    def __init__(self):
        print("로지스틱 회귀 모델이 생성되었습니다.")
        self.model = None
        self.x_scaler = None
        self.y_scaler = None

    def train(self, x_train, y_train):
        model = LogisticRegression()
        model.fit(x_train, y_train)
        print("모델 학습 완료!")

        self.model = model

    def get_score(self, x, y):
        score = self.model.score(x, y)
        print(f"모델 평가 점수는 {score:.3f}점 입니다.")

        return score

    def scale_input_data(self, x):
        """
        sklearn의 MinMaxScaler를 활용한다.
        input data를 scaling한다.
        :param x: input data
        :param scaler: scaler
        :return: scaled input data, scaler
        """
        if self.x_scaler == None:
            scaler = MinMaxScaler()
            scaled_x = scaler.fit_transform(x)
            self.x_scaler = scaler
        else:
            scaled_x = self.x_scaler.transform(x)

        return scaled_x


class NeuralNet():
    """
    신경망 모델 만들기
    """
    def __init__(self):
        pass

class KNN():
    """
    K-NN 모델 만들기
    """
    def __init__(self):
        pass