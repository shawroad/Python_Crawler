from lxml import etree
import requests
from selenium import webdriver
import time
import random
import csv



def login(driver):
    driver.get('https://weibo.com')
    time.sleep(3)
    # 设置窗口的尺寸 防止尺寸不够影响我们提取内容
    driver.set_window_size(1920, 1080)

    # 找到用户输入框
    username = driver.find_element_by_xpath('//*[@id="loginname"]')
    username.send_keys('*******')
    password = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
    password.send_keys('*****')
    submit = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
    print("一切输入准备好了，点击登录")
    submit.click()
    time.sleep(random.randint(2, 5))


def spider(driver):
    # 1.刷新首页
    driver.get('https://weibo.com')
    # 随机停几秒
    time.sleep(random.randint(2, 6))
    # 先获取所有微博代码
    all_weibo = driver.find_elements_by_xpath('//div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like"]')

    for weibo in all_weibo:
        # 注意webdriver中xpath用法

        # 解析id  提取文本
        pubid = weibo.find_elements_by_xpath('div[1]/div[3]/div[1]/a[1]')[0].text
        # 解析微博链接  提取属性值
        pubid_url = weibo.find_elements_by_xpath('div[1]/div[3]/div[1]/a[1]')[0].get_attribute('href')
        # 解析微博内容
        pub_content = weibo.find_elements_by_xpath('div[1]/div[3]/div[3]')[0].text
        item = [pubid, pubid_url, pub_content]
        data_csv(item)

def data_csv(item):
    with open('新浪微博爬取.csv', 'a', encoding='gbk', newline='') as csvfile:
        writer = csv.writer(csvfile)
        try:
            # 因为提取的内容gbk解码不了  然后就会报错。我们可以忽略这个错误
            writer.writerrow(item)
        except:
            print("写入失败")
if __name__ == '__main__':
    # 实例化webdriver
    driver = webdriver.Chrome(r'D:\learnsofeware\python3.5\chromedriver.exe')

    driver.implicitly_wait(10)  # 隐式等待时间为10秒 若10秒反应则报错
    login(driver)  # 执行登录
    while True:
        spider(driver)  # 进入主页进行内容的爬取
        time.sleep(600)