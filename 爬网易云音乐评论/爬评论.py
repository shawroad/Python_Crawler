"""

@file   : 爬评论.py

@author : xiaolu

@time   : 2019-11-25

"""
from Crypto.Cipher import AES
import base64
import requests
import json
import time
import random
from bs4 import BeautifulSoup
import glob
import os


headers = {
    'Host': 'music.163.com',
    'Origin': 'https://music.163.com',
    'Referer': 'https://music.163.com/song?id=28793052',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

# 除了第一个参数，其他参数为固定参数，可以直接套用
# offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
# 第一个参数
# first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
# 第二个参数
second_param = "010001"
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"


# 获取参数
def get_params(page):  # page为传入页数
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if page == 1:  # 如果为第一页
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset, 'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = str(encrypt_text, encoding="utf-8") 　
    return encrypt_text


# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


def get_all_comments(url, page):
    all_comments_list = []   # 存放当前歌曲的所有评论
    for i in range(page):
        time.sleep(random.randint(5, 15))  # 随机休息
        params = get_params(i + 1)
        encSecKey = get_encSecKey()
        json_text = get_json(url, params, encSecKey)  # 发送的请求
        json_dict = json.loads(json_text)

        for item in json_dict['comments']:
            comment = item['content']  # 评论内容
            comment_info = str(comment)
            all_comments_list.append(comment_info)
        print('当前歌曲第%d页抓取完毕!' % (i+1))
    return all_comments_list


def crawl(tokens):

    k = 0
    for token in tokens:
        k += 1
        print("正在爬去第{}首歌".format(k))
        # 给定一首歌的链接 这里要给的是R_SO的链接   通过network中的xhr获得
        url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(token)  # 替换为你想下载的歌曲R_SO的链接
        all_comments_list = get_all_comments(url, page=10)  # 需要前十页的评论
        comment_song = '\n'.join(all_comments_list)
        with open('./{}/{}.txt'.format(p[:-4], k), 'w') as f:
            f.write(comment_song)


def load_ids(p):
    os.makedirs(p[:-4])
    print("正在爬去{}歌曲".format(p[:-4]))

    with open(p, 'r') as f:
        temp = []
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            temp.append(line)
        crawl(temp)


if __name__ == '__main__':
    path = glob.glob('*.txt')
    for p in path:
        load_ids(p)
