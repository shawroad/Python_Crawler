import requests
from lxml import etree
import time
import random
import csv


# # 定义代理Ip列表
#     Proxies = [
#         {"https": "https://182.88.184.207:9797"},
#         {"https": "https://112.95.23.1:8888"},
#         {"https": "https://14.20.235.169:30862"},
#         {"https": "https://123.139.56.238:9999"},
#         {"https": "https://221.7.211.246:60233"},
#     ]
#  response = requests.get(url, proxies=random.choice(Proxies), headers=headers)
def spider():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    url = 'https://www.xicidaili.com/nt/{}'
    # 爬取10页的代理
    for i in range(1, 2):    
        response = requests.get(url.format(i), headers = headers)
        selector = etree.HTML(response.text)
        type1 = selector.xpath('//tr[@class="odd"]')
        type2 = selector.xpath('//tr[@class=""]')
        type1.extend(type2)
        ip_pool = []
        for t1 in type1:
            ip_ = t1.xpath('td[2]/text()')[0]
            port_ = t1.xpath('td[3]/text()')[0]
            procol_ = t1.xpath('td[6]/text()')[0]
            procol_ = procol_.lower()
            item = {}
            item[procol_] = procol_+":"+ "//"+ip_ + ":"+ port_
            ip_pool.append(item)
        print(ip_pool)
        return ip_pool

def try_csdn(ip_pool):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    url = 'https://blog.csdn.net/shawroad88/article/details/88785869'
    valid_ip = []
    for pro in ip_pool:
        try:
            print("无效ip:", pro)
            response = requests.get(url, headers=headers, proxies=pro, timeout=(4, 7))
            if response.status_code == 200:
                print("有效ip:", pro)
                valid_ip.append(pro)
        except Exception:
            pass
    return valid_ip
        
def data_csv(item):
    with open('./有效代理.csv', 'wb', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(item)


if __name__ == '__main__':
    ip_pool = spider()
    valid_ip = try_csdn(ip_pool)
    # 将返回的有效代理存到csv文件中
    for item in valid_ip:
        data_csv(item)
