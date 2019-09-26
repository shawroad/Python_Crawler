"""

@file  : 011-爬唯美的句子.py

@author: xiaolu

@time  : 2019-09-26

"""
import requests
import random
import time
from lxml import etree
import pandas as pd


def save_data(content_list):
    '''
    保存数据
    :param content_list:
    :return:
    '''
    name = ['语料']
    temp = pd.DataFrame(columns=name, data=content_list)
    temp.to_csv('./唯美{}.csv'.format(len(content_list)))


def crawl_text():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

    total_text = []
    for i in range(1, 439):
        # url = 'https://www.duanwenxue.com/yuju/weimei/list_{}.html'.format(i)
        url = 'https://www.duanwenxue.com/yuju/yulu/list_{}.html'.format(i)
        # url = 'https://www.duanwenxue.com/yuju/weimei/list_1.html'
        response = requests.get(url, headers)
        selector = etree.HTML(response.text)
        list_text = selector.xpath('//div[@class="list-short-article"]/ul/li')
        # print(list_text)
        time.sleep(random.randint(2, 4))

        j = 0
        for li in list_text:

            time.sleep(random.randint(2, 4))

            j += 1
            text = li.xpath('p/a/text()')[0]
            print("爬去第{}页,第{}条数据,数据为:{}".format(i, j, text))

            total_text.append(text)

            if len(total_text) % 100 == 0:
                save_data(total_text)


if __name__ == '__main__':
    # 爬更多的夸夸
    crawl_text()

