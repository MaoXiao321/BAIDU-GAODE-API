# -*- coding: utf-8 -*-

"""
代码功能：坐标转换（墨卡托平面坐标）
https://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition
"""

import pandas as pd
import json
from urllib.request import urlopen


def coordinateTrans(df):
    x_ls, y_ls = [],[]
    for i in range(len(df)):
        lat = str(df.loc[i, 'lat'])
        lon = str(df.loc[i, 'lon'])
        url = f"https://api.map.baidu.com/geoconv/v1/?coords={lon},{lat}&from=1&to=6&ak={ak}"
        result = json.loads(urlopen(url).read())  # json转dict
        status = result['status']
        if status == 0:  # 状态码为0：成功
            x = result['result'][0]['x']  # 经度
            y = result['result'][0]['y']  # 纬度
        else:  # 1:服务器内部错误;2:参数错误
            try:
                x, y = result['message'],result['message']
            except Exception as e:
                x, y = 'error','error'
                print(f"第{i}行无结果----")
        x_ls.append(x)
        y_ls.append(y)
    # 输出结果
    df['x'], df['y'] = x_ls, y_ls
    df.to_excel('坐标转换.xlsx', index=False)

if __name__ == '__main__':
    ak = '111'
    df = pd.read_excel("经纬度.xlsx")
    coordinateTrans(df)
