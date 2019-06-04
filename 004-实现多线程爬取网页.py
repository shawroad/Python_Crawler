from multiprocessing.dummy import Pool as pl

import requests
from lxml import etree
import time

count = 0

def spider(url):
    global count   # 定义这个东西就是为了让图片的名字不能重复
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)
    for j in range(1, 31):
        # 获取每张图片的url
        count += 1
        url_iamge = selector.xpath('//*[@id="houselist-mod-new"]/li[{}]/div[1]/img/@src'.format(j))[0]
        res = requests.get(url_iamge, headers=headers)
        #  这里要注意图片的名字不能重复

        with open("./安居客/{}.jpg".format(str(count)), 'wb') as f:
            f.write(res.content)   # 把图片内容写入
        time.sleep(2)

    # 爬完休息一会
    time.sleep(2)

if __name__ == "__main__":
    pool = pl(4)  # 初始化线程池
    preurl = 'https://xa.anjuke.com/sale/p{}/?pi=baidu-cpc-xa-tyongxa1&kwid=89460384111#filtersort'
    house_url = [preurl.format(i) for i in range(1, 5)]   # 用列表推导式搞出10页的url

    # 将url映射给spider
    pool.map(spider, house_url)
    pool.close()
    pool.join()

