"""

@file   : 010-爬彩虹屁.py

@author : xiaolu

@time   : 2019-09-24

"""
from selenium import webdriver
import time
import random
import pandas as pd


def save_data(content, i):
    name = ['语料']
    temp = pd.DataFrame(columns=name, data=content)
    temp.to_csv('./corpus{}.csv'.format(i))


def spider(driver):
    # 1. 刷新首页
    driver.get('https://chp.shadiao.app/')

    corpus = []
    i = 0
    while True:
        # 随机停几秒
        i += 1
        time.sleep(random.randint(2, 6))
        data = driver.find_element_by_xpath('//*[@id="txt_nmsl"]').text
        corpus.append(data)
        submit = driver.find_element_by_xpath('//*[@id="btn_random"]/span[2]')
        submit.click()

        print("当前第{}语料:{}".format(i, data))

        if i % 50 == 0:
            save_data(corpus, i)


if __name__ == '__main__':
    # 实例化webdriver
    driver = webdriver.Chrome(r'D:\learn-install\python3.6\chromedriver.exe')
    spider(driver)
