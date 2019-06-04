import requests
from lxml import etree
import csv
import time

def spider():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    # 我们爬去前10页的房源信息
    for i in range(1, 3):
        print("正在爬取{}页".format(i))
        url = 'https://xa.anjuke.com/sale/p{}/?pi=baidu-cpc-xa-tyongxa1&kwid=89460384111#filtersort'.format(i)
        response = requests.get(url, headers=headers)

        selector = etree.HTML(response.text)
        for j in range(1, 31):
            # 获取每张图片的url
            url_iamge = selector.xpath('//*[@id="houselist-mod-new"]/li[{}]/div[1]/img/@src'.format(j))[0]
            res = requests.get(url_iamge, headers=headers)
            with open("./安居客/{}.jpg".format(str(i)+str(j)), 'wb') as f:
                f.write(res.content)   # 把图片内容写入
            time.sleep(2)

        # 爬完休息一会
        time.sleep(2)

if __name__ == "__main__":
    spider()