"""

@file   : 008-爬网页用bs4所有图片url.py

@author : xiaolu

@time1  : 2019-06-05

"""
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


def spider():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    url = 'http://www.winhye.com/goods/show-111.html'
    response = requests.get(url, headers=headers)
    response = response.text

    soup = BeautifulSoup(response)
    img = soup.find_all('img')
    # print(img)   # 看一下提取的东西
    # 类似于<img alt="" height="270" src="http://www.novish.cn/upload/img/201711071141264001.jpg" width="479"/>

    # 将提取的内容清洗一下
    url = []
    for item in img:
        item = str(item)
        temp = item.replace('<img ', '').replace('/>', '').split(' ')
        for t in temp:
            title, cont = t.split('=')
            if title == "src":
                url.append(cont)

    # 过滤url
    filter_url = []
    for u in url:
        t = list(u)

        if ''.join(t[1:5]) == 'http':
            filter_url.append(u)

    # 打印出所有提取的url
    for url in filter_url:
        print("图片的url:", url)


if __name__ == '__main__':
    spider()

