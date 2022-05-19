# -*- coding: utf-8 -*-

"""
代码功能：
算输入文件中的坐标到给定目标点的路线距离(米)
百度API开发文档：https://lbsyun.baidu.com/index.php?title=webapi/route-matrix-api-v2
"""

from json.tool import main
import pandas as pd
import json
from urllib.request import urlopen


def get_distance(df):
    ls = []
    destination = '31.2317,121.4564'  
    for i in range(len(df)):
        lat = str(df.loc[i, 'lat'])
        lon = str(df.loc[i, 'lon'])
        url = f"https://api.map.baidu.com/routematrix/v2/driving?output=json&" \
            f"origins={lat},{lon}&destinations={destination}&ak={ak}"
        result = json.loads(urlopen(url).read())  # json转dict
        status = result['status']
        if status == 0:  # 状态码为0：成功
            distance = result['result'][0]['distance']['value']  # 里程(米)
        else:  # 1:服务器内部错误;2:参数错误
            try:
                distance = result['message']
            except Exception as e:
                distance = 0
                print(f"第{i}行无结果----")
        ls.append(distance)
    df['路线距离(米)'] = ls
    df.to_excel('路线距离(米).xlsx', index=False)


if __name__ == '__main__':
    ak = 'TZtttx9HT5DCrXdeA0TMG9TsgsbRdKmE'
    df = pd.read_excel("经纬度.xlsx")
    get_distance(df)

