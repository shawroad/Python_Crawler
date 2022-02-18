"""
@file   : run_spider_huawei_top.py.py
@author : xiaolu
@email  : luxiaonlp@163.com
@time   : 2022-02-16
"""

import time
import requests
import pandas as pd


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    final_data = []
    final_app_name, final_app_cls = [], []
    for i in range(1, 16):
        time.sleep(2)
        url = 'https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum={}&uri=automore%7Cdoublecolumncardwithstar%7C903178%7CPC1000&maxResults=25&zone=&locale=zh'.format(i)
        response = requests.get(url, headers)
        data = response.json()

        for item in data['layoutData'][0]['dataList']:
            app_name = item['name'].strip()
            kind_name = item['kindName'].strip()
            final_app_name.append(app_name)
            final_app_cls.append(kind_name)
    df = pd.DataFrame({'app': final_app_name, 'label': final_app_cls})
    df.to_csv('crawl_app_data_huawei.csv', index=False)

