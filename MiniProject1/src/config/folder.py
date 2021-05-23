# coding=utf-8
"""
-----------------------------------------------------------------------------------
# Description:

파일의 상대경로 설정

-----------------------------------------------------------------------------------
"""

import os

base = os.path.dirname(__file__).replace("/src/config", "").replace("\\src\\setting", "")
src = os.path.join(base, 'src')
data = os.path.join(base, 'data')
data_process = os.path.join(src, 'data_process')
eda = os.path.join(src, 'eda')
gui = os.path.join(src, 'gui')
model = os.path.join(src, 'model')

def get_data_path(file_name: str):
    """
    /data에 존재할, 혹은 존재하는 파일의 위치를 반환
    :param file_name: /data에 위치할, 혹은 위치하는 파일명
    """
    file_path = os.path.join(data, file_name)

    return file_path