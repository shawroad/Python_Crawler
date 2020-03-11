"""

@file  : 016-爬去豆瓣电影影评.py

@author: xiaolu

@time  : 2020-03-02

"""
'https://movie.douban.com/subject/30306570/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h'
'https://movie.douban.com/subject/26885074/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h'
import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re
import time
import random
import json


s = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


def sign_in():
    global headers
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    data = {
        'name': "**********",
        "password": "***********",
        "remember": "false"
    }
    r = s.post(url, headers=headers, data=data, verify=False)

    if 'your name' in r.text:
        print('登录成功')
    else:
        print('登录失败')


def crawl_id():
    global headers
    base_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}'
    id_list = []
    for i in range(0, 1001, 20):
        print('爬去第{}页电影的id号'.format(int(i / 20)))
        time.sleep(random.random() * 5)

        url = base_url.format(i)
        text = s.get(url, headers=headers).content
        text = str(text)
        ids = re.findall(r'"id":"[0-9]{8}"', text)
        if len(ids) == 0:
            break

        for id in ids:
            temp = re.findall('[0-9]{8}', id)[0]
            id_list.append(temp)

    idstr = '\n'.join(id_list)
    with open('id.txt', 'w') as f:
        f.write(idstr)

    return id_list


def crawl_content(id):
    global headers

    # 1. 爬去好评
    h_url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=h'

    data = []
    for i in range(0, 1000, 20):
        print('正在爬去好评{}页'.format(int(i / 20)))
        time.sleep(random.random() * 5)
        # print(h_url.format(id, i))
        text = s.get(h_url.format(id, i), headers=headers).content
        soup = BeautifulSoup(text, features='lxml')
        lists = soup.find_all('span', {'class': 'short'})
        if len(lists) == 0:
            break

        for l in lists:
            content = l.contents[0].replace('\n', '')
            data.append(content)
    data = '\n'.join(data)
    with open('positive.txt', 'a+', encoding='utf8') as f:
        f.write(data)

    # 2.爬取中评
    m_url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=m'
    data = []
    for i in range(0, 1000, 20):
        print('正在爬去中评{}页'.format(int(i / 20)))
        time.sleep(random.random() * 5)
        # print(m_url.format(id, i))
        text = s.get(m_url.format(id, i), headers=headers).content
        soup = BeautifulSoup(text, features='lxml')
        lists = soup.find_all('span', {'class': 'short'})
        if len(lists) == 0:
            break

        for l in lists:
            content = l.contents[0].replace('\n', '')
            data.append(content)
    data = '\n'.join(data)
    with open('neutral.txt', 'a+', encoding='utf8') as f:
        f.write(data)

    # 3.爬取差评
    l_url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=l'
    data = []
    for i in range(0, 1000, 20):
        print('正在爬去差评{}页'.format(int(i / 20)))
        time.sleep(random.random() * 5)
        # print(m_url.format(id, i))
        text = s.get(l_url.format(id, i), headers=headers).content
        soup = BeautifulSoup(text, features='lxml')
        lists = soup.find_all('span', {'class': 'short'})
        if len(lists) == 0:
            break

        for l in lists:
            content = l.contents[0].replace('\n', '')
            data.append(content)
    data = '\n'.join(data)
    with open('negative.txt', 'a+', encoding='utf8') as f:
        f.write(data)


if __name__ == '__main__':
    # 第一步:登录
    sign_in()

    # 第二步:爬取电影对应的id  有点问题
    sign = True   # 是否去爬id
    if sign:
        id_list = crawl_id()
    else:
        id_list = []
        with open('id.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                id_list.append(line)

    
    # 第三步:根据id爬去对应的影评
    i = 1
    for id in id_list:
        print('爬取第{}部电影'.format(i))
        crawl_content(id)
        i += 1


