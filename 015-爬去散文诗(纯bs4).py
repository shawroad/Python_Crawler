"""

@file  : 015-爬去散文诗(纯bs4).py

@author: xiaolu

@time  : 2019-11-26

"""
import time
import random
import requests
from bs4 import BeautifulSoup


def save_data(content, i):
    with open('{}corpus.data'.format(i), 'w', encoding='utf8', errors='ignore') as f:
        f.write(content)


i = 0


def spider(lists):
    global i
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    for list in lists:
        i += 1
        time.sleep(random.randint(5, 10))
        response = requests.get(list, headers)
        response.encoding = 'utf8'
        html = response.text
        soup = BeautifulSoup(html, features='lxml')
        temp = soup.find_all('div', {'class': "m-lg font14"})

        p_page = temp[0].find_all('p')
        data = [p.text for p in p_page]
        data = '\n'.join(data)

        print("文章{}正在保存...".format(i))
        save_data(data, i)


def crawl_link():
    '''
    爬去链接
    :return:
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    for j in range(2, 19):
        url = 'http://www.zgshige.com/mjxzx/index_{}.shtml'.format(j)
        response = requests.get(url, headers)
        html = response.text

        soup = BeautifulSoup(html, features='lxml')
        temp = soup.find_all('ul', {'class': 'list-unstyled lh20'})

        links = temp[0].find_all('a', {'class': "h4 bold"})

        total_links = ['http://www.zgshige.com' + _['href'] for _ in links]
        print("当前页数:{}".format(j))
        print("总链接数:{}".format(len(total_links)))

        spider(total_links)


if __name__ == '__main__':
    crawl_link()
