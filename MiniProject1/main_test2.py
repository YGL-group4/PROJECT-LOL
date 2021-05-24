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
# from MiniProject1.src.data_process import summoners
# from MiniProject1.src.data_process import crawling
# from MiniProject1.src.data_process import formatter
# from MiniProject1.src.model import modeling

import pandas as pd
from MiniProject1.src.config import folder
path = folder.get_data_path('challenger_0521.csv')
data = pd.read_csv(path, index_col=0)



data = formatter.longer_playtime(data, '20:00')

# get only one position
data = data[data['position'] == self.position]
data = data.drop(['position'], axis=1)