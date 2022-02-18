"""
@file   : run_spider.py
@author : xiaolu
@email  : luxiaonlp@163.com
@time   : 2022-02-15
"""
import time
import random
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def input_user_password():
    # 去妙笔网站注册账号  然后替换成自己的用户名和密码
    user = 'xxxxx@qq.com'
    pwd = '******'   
    url1 = 'https://cc.oceanengine.com/login'
    driver.get(url1)
    time.sleep(5)
    input_user = driver.find_element_by_name('email')
    input_user.send_keys(user)

    input_pwd = driver.find_element_by_name('password')
    input_pwd.send_keys(pwd)

    driver.find_element_by_xpath('//*[@id="cc-login"]/section/div[6]/button').click()


if __name__ == '__main__':
    # 0. 加载app词
    app_vocab = ['王者荣耀', '叮咚买菜', '微信', '抖音短视频']

    # 1. 打开浏览器 并登录账号
    driver = webdriver.Chrome('./chromedriver')
    input_user_password()   # 登录账号

    # 2. 进入妙笔的网页
    time.sleep(5)
    miaobi_url = 'https://cc.oceanengine.com/creative-factory/miaobi'
    driver.get(miaobi_url)
    time.sleep(10)

    # 3. 获取内嵌子网页
    frame = driver.find_elements_by_tag_name('iframe')
    driver.switch_to.frame(frame[0])

    # 4. 点击下来框 选定"不限"
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/input').click()
    time.sleep(3)
    # 选择对应的类别 "不限"
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div/div[1]/ul/li[1]/span').click()
    time.sleep(3)

    # 5. 这里写个循环  开始输入关键词 得到
    res = {}
    for vocab in app_vocab:
        print(vocab)
        # 5.1 输入关键词
        input_keyword = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[1]/div[2]/div[2]/div[2]/input')
        input_keyword.send_keys(vocab)
        time.sleep(random.randint(2, 4))
        # 5.2 提交 生成广告
        driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[1]/div[2]/button').click()
        time.sleep(random.randint(3, 5))
        selenium_select = driver.find_elements(by=By.CLASS_NAME, value='title-create__right-copy-button')
        ad_list = []
        for sel in selenium_select:
            ad = sel.get_attribute('data-clipboard-text')
            ad_list.append(ad)
        res[vocab] = ad_list
        input_keyword.clear()
        time.sleep(random.randint(2, 4))
    json.dump(res, open('./result.json', 'w', encoding='utf8'), ensure_ascii=False)

