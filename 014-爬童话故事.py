"""

@file   : 014-爬童话故事.py

@author : xiaolu

@time   : 2019-10-29

"""
import requests
import random
import time
from lxml import etree
from bs4 import BeautifulSoup
import re
import os


def sava_data(title, content, i):
    '''
    存数据
    :param title:
    :param content:
    :return:
    '''
    if not os.path.exists('./睡前故事/{}page'.format(i)):
        os.mkdir('./睡前故事/{}page'.format(i))
    else:
        pass
    with open('./睡前故事/{}page/{}.txt'.format(i, title), 'w', errors='ignore') as f:
        f.write(content)


def crawl_content(links, i):
    '''
    爬取内容
    :param links:
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

    for temp in links:
        time.sleep(random.randint(8, 20))
        response = requests.get(temp, headers)
        response.encoding = 'gbk'

        selector = etree.HTML(response.text)

        try:
            title = selector.xpath('//*[@id="left"]/h1/text()')[0]
            content = selector.xpath('string(//*[@id="ny"])')
            print("当前页:{}, 文章:{}".format(i, title))
            sava_data(title, content, i)
        except:
            pass


def crawl_link():
    '''
    爬取相应的链接
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    for i in range(1, 96):
        print("当前页: {}".format(i))
        # 经典童话:http://www.etgushi.com/jdth/list_1_{}.html
        # 儿童故事:http://www.etgushi.com/etgs/list_4_{}.html
        # 睡前故事:http://www.etgushi.com/sqgs/list_7_{}.html
        url = 'http://www.etgushi.com/sqgs/list_7_{}.html'.format(i)

        response = requests.get(url, headers)
        html = response.text

        soup = BeautifulSoup(html, features='lxml')

        # href="/etgs/6950.html"
        # href="/sqgs/6813.html"
        links = soup.find_all('a', {'target': "_blank", 'href': re.compile('/sqgs/.*.html')})
        total_links = ['http://www.etgushi.com' + _['href'] for _ in links]
        total_links = list(set(total_links))
        print("总共链接数:{}".format(len(total_links)))
        print(total_links)
        crawl_content(total_links, i)


if __name__ == '__main__':
    crawl_link()
