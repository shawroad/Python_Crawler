"""

@file   : 012-bs+selenium爬数据.py

@author : xiaolu

@time   : 2019-10-23

"""
from selenium import webdriver
import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def save_data(content, i):
    with open('{}corpus.data'.format(i), 'w', errors='ignore') as f:
        f.write(content)


def spider(driver, lists):
    # 1. 刷新首页
    i = 0
    for list in lists:
        driver.get(list)
        # 随机停几秒
        i += 1
        time.sleep(random.randint(5, 10))
        # /html/body/div[7]/div[1]/div[1]/h1
        # data = driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[1]/h1/text()')[0]
        data = driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[1]/div[2]').text
        save_data(data, i)


def crawl_link():
    '''
    爬去链接
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    url = 'https://www.duanwenxue.com/sanwen/youmei/list_8.html'
    response = requests.get(url, headers)
    html = response.text

    soup = BeautifulSoup(html, features='lxml')

    # <a target="_blank" href="/article/4881118.html">小城记忆</a>
    links = soup.find_all('a', {'href': re.compile('/article/.*')})
    total_links = ['https://www.duanwenxue.com' + _['href'] for _ in links]
    print(total_links)

    return total_links


if __name__ == '__main__':
    # 实例化webdriver
    lists = crawl_link()
    driver = webdriver.Chrome(r'D:\learn-install\python3.6\chromedriver.exe')
    spider(driver, lists)
