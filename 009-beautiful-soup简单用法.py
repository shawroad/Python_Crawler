"""

@file   : 009-beautiful-soup简单用法.py

@author : xiaolu

@time   : 2019-06-19

"""
from bs4 import BeautifulSoup
import requests
import re


# # 爬取指定连接   返回response
# response = requests.get('https://morvanzhou.github.io/static/scraping/basic-structure.html')
#
# html = response.text
#
# soup = BeautifulSoup(html, features='lxml')
# # 提取出指定标签
# print(soup.h1)
# print(soup.p)
#
#
# # 查找全部的a标签
# all_href = soup.find_all('a')   # 查找所有a标签
# all_href = [_['href'] for _ in all_href]
# print('\n'.join(all_href))



# response = requests.get("https://morvanzhou.github.io/static/scraping/list.html")
# html = response.text
# soup = BeautifulSoup(html, features='lxml')
#
# # 使用class去限制搜索   只找class属性值为month为li标签
# month = soup.find_all('li', {"class": "month"})
# for m in month:
#     print(m)    # 这个是提取整个标签
#     print(m.get_text())   # 这个是提取标签下的文本
#
# jan = soup.find('ul', {'class': 'jan'})
# d_jan = jan.find_all('li')   # use jan as a parent
# for d in d_jan:
#     print(d.get_text())




# # bs4+regex的用法
# response = requests.get("https://morvanzhou.github.io/static/scraping/table.html")
# html = response.text
# soup = BeautifulSoup(html, features='lxml')
#
# # 找图片的链接
# img_links = soup.find_all('img', {"src": re.compile('.*?\.jpg')})
# for link in img_links:
#     print(link['src'])
#
# print('\n')
#
# course_links = soup.find_all('a', {'href': re.compile('https://morvan.*')})
# for link in course_links:
#     print(link['href'])



response = requests.get("https://morvanzhou.github.io/static/scraping/table.html")
html = response.text
soup = BeautifulSoup(html, features='lxml')
for item in soup.find('table', {"id": "course-list"}).children:
    print(item)

for item in soup.find("table", {"id": "course-list"}).tr.next_siblings:
    print(item)

