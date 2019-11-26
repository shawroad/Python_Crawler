"""

@file   : 爬R_SOid号.py

@author : xiaolu

@time   : 2019-11-25

"""
from selenium import webdriver
import time
import random
import pandas as pd
from bs4 import BeautifulSoup


def spider(driver):
    # 1. 刷新首页
    driver.get('https://music.163.com/#/discover/toplist?id=71385702')

    driver.switch_to_frame('g_iframe')

    html = driver.page_source

    soup = BeautifulSoup(html)
    sign = soup.find_all('span', {"data-res-action": "play"})
    ids = [_["data-res-id"] for _ in sign]
    ids = '\n'.join(ids)
    with open('云音乐ACG音乐榜.txt', 'w') as f:
        f.write(ids)
    exit()


if __name__ == '__main__':
    # 实例化webdriver
    driver = webdriver.Chrome(r'D:\learn-install\python3.6\chromedriver.exe')
    spider(driver)

