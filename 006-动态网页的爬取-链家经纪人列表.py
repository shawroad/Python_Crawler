# https://m.lianjia.com/xa/jingjiren/?page_size=15&_t=1&offset=15
# https://m.lianjia.com/xa/jingjiren/?page_size=15&_t=1&offset=30
# 上面两次ajax请求的实际url
# 我们可以从中发现，每次改变的只是offset的值  每次加15  初始的offset值为0
# 开始干活   我们提取出链家经纪人的名字
import requests
from lxml import etree
import time
import random
import csv


def spider():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    url = 'https://m.lianjia.com/xa/jingjiren/?page_size=15&_t=1&offset={}'
    for i in range(0, 151, 15):   # 爬取10页
        response = requests.get(url.format(i), headers=headers)
        selector = etree.HTML(response.text)
        print("正在爬取第{}页".format((i // 15) + 1))
        # 解析出所有经济人的li标签
        agent_list = selector.xpath('//li[@class="pictext flexbox box_center_v lazyload_ulog"]')

        for agent in agent_list:
            agent_name = agent.xpath('div/div[2]/div[1]/span[1]/a/text()')[0].strip().replace('\n', '')
            agent_career = agent.xpath('div/div[2]/div[1]/span[2]/text()')[0].strip().replace('\n', '')
            agent_region = agent.xpath('div/div[2]/div[2]/span[1]/text()')[0].strip().replace('\n', '')
            agent_shop = agent.xpath('div/div[2]/div[2]/span[3]/text()')[0].strip().replace('\n', '')
            agent_list = [agent_name, agent_career, agent_region, agent_shop]
            # 将数据写入csv文件中
            data_save(agent_list)

        time.sleep(random.randint(2, 5))
def data_save(item):
    with open('经纪人.csv', 'a', encoding='gbk', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(item)

if __name__ == '__main__':
    spider()
