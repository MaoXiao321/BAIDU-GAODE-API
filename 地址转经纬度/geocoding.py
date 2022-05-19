
"""
代码功能：地理编码
https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
"""

import pandas as pd
import json
import requests
from urllib.parse import quote
import os

def geocoding(df, ak):
    x_ls, y_ls = [], []
    for i in range(len(df)):
        addr = df.loc[i, '地址']  # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
        print(addr)
        url = f"https://api.map.baidu.com/geocoding/v3/?address={addr}&city='上海市'&output=json&ak={ak}" \
              f"&callback=showLocation"

        r = requests.get(url)
        r = r.text

        '''经历以下两次去除，使得最终结果为json格式的数据 
           原来的数据格式：showLocation&&showLocation(' showLocation&&showLocation('showLocation&&showLocation({"status":0,"result":{"location":{"lng":108.94646555063274,"lat":34.34726881662395},"precise":0,"confidence":12,"comprehension":63,"level":"城市"}}）
           去除后的数据格式为将json字符串转换为字典类型：showLocation&&showLocation({"status":0,"result":{"location":{"lng":108.94646555063274,"lat":34.34726881662395},"precise":0,"confidence":12,"comprehension":63,"level":"城市"}}
        '''
        r = r.strip('showLocation&&showLocation(')
        r = r.strip(')')
        result = json.loads(r)  # json转dict
        status = result['status']
        if status == 0:  # 状态码为0：成功
            x = result['result']['location']['lng']  # 经度
            y = result['result']['location']['lat']  # 纬度
        else:  # 1:服务器内部错误;2:参数错误
            try:
                x, y = result['message'], result['message']
            except Exception as e:
                x, y = 'error', 'error'
                print(f"第{i}行无结果----")
        x_ls.append(x)
        y_ls.append(y)
    df['x'], df['y'] = x_ls, y_ls
    return df


if __name__ == '__main__':
    ak = '111'
    df = pd.read_excel("./地址.xlsx")  # 必须有地址列
    df.index = range(len(df))
    result = geocoding(df, ak)
    result.to_excel('./经纬度.xlsx', index=False)
