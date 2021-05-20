import os

base = os.path.dirname(__file__).replace("/setting", "").replace("\\setting", "")
data = os.path.join(base, 'data')

def get_data_path(file_name: str):
    """
    /data에 존재할, 혹은 존재하는 파일의 위치를 반환
    :param file_name: /data에 위치할, 혹은 위치하는 파일명
    """
    file_path = os.path.join(data, file_name)

    return file_path