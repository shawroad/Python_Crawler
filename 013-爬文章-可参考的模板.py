"""

@file   : 013-爬文章-可参考的模板.py

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
    title = re.sub(r'[^a-zA-Z.!?\', "0-9:;-]+', r'', title)

    if not os.path.exists('./儿童笑话/{}page'.format(i)):
        os.mkdir('./儿童笑话/{}page'.format(i))
    else:
        pass

    title = str(title)
    temp_list = []
    if len(title) != 0:
        for t in list(title):
            if t == '>' or t == '<' or t == '?':
                temp_list.append('_')
            else:
                temp_list.append(t)
        title = ''.join(temp_list)
        with open('./儿童笑话/{}page/{}.txt'.format(i, title), 'w', errors='ignore') as f:
            f.write(content)


def crawl_content(links, i):
    '''
    爬取内容
    :param links:
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

    for temp in links:
        time.sleep(random.randint(10, 30))
        response = requests.get(temp, headers)
        selector = etree.HTML(response.text)
        try:
            title = selector.xpath('//*[@id="wenzhangziti"]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/font/text()')[0]
            content = selector.xpath('string(//*[@id="dede_content"])')
            print(title)
            sava_data(title, content, i)
        except:
            pass


def crawl_link():
    '''
    爬取相应的链接
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    for i in range(11, 49):
        print("当前页: {}".format(i))
        # 童话故事:http://www.enread.com/story/fairy/list_{}.html
        # 情感故事:http://www.enread.com/story/love/list_{}.html
        # 寓言故事:http://www.enread.com/story/fable/list_{}.html
        # 名人传记:http://www.enread.com/story/biography/list_{}.html
        # 双语故事:http://www.enread.com/story/shuangyu/list_{}.html
        # 儿童笑话:http://www.enread.com/humors/kids/list_{}.html
        url = 'http://www.enread.com/humors/kids/list_{}.html'.format(i)

        response = requests.get(url, headers)
        html = response.text

        soup = BeautifulSoup(html, features='lxml')

        # href="/story/fairy/105470.html"
        # href="/story/love/92984.html"
        # href="/story/fable/102520.html"
        # href="/humors/kids/103886.html"
        links = soup.find_all('a', {'href': re.compile('/humors/kids/.*.html')})
        # http://www.enread.com
        total_links = ['http://www.enread.com' + _['href'] for _ in links]
        total_links = list(set(total_links))
        print("总共链接数:{}".format(len(total_links)))
        print(total_links)
        crawl_content(total_links, i)


if __name__ == '__main__':
    crawl_link()
