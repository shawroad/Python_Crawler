"""
@file   : run_spider_xiaomi_top100_app.py
@author : xiaolu
@email  : luxiaonlp@163.com
@time   : 2022-02-16
"""

import time
import requests
from lxml import etree
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    final_data = []
    for i in range(1, 4):
        url = 'https://app.mi.com/catTopList/0?page={}'.format(i)
        response = requests.get(url, headers)
        time.sleep(3)
        selector = etree.HTML(response.text)
        for j in range(1, 37):
            app_name = selector.xpath('/html/body/div[6]/div/div[1]/div[1]/ul/li[{}]/h5/a/text()'.format(j))[0]
            app_cls = selector.xpath('/html/body/div[6]/div/div[1]/div[1]/ul/li[{}]/p/a/text()'.format(j))[0]
            s = app_name.strip() + '\t' + app_cls.strip()
            final_data.append(s)
    print(len(final_data))
    with open('app_crawl_data.txt', 'w', encoding='utf8') as f:
        f.write('\n'.join(final_data))
