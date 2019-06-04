import requests
from lxml import etree



def cookie_parse(cookie):
    coo = {}
    temp = cookie.strip().split(';')
    for item in temp:
        hah = item.split('=')
        hah[0] = hah[0].strip()
        hah[1] = hah[1].strip()
        coo[hah[0]] = hah[1]
    return coo

def denglu(cookies):
    url = 'https://www.douban.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    response = requests.get(url, headers=headers, cookies=cookies)

    selector = etree.HTML(response.text)
    name = selector.xpath('//*[@id="db-global-nav"]/div/div[1]/ul/li[2]/a/span[1]/text()')[0]

    print(name)


if __name__ == '__main__':

    cookie = 'll="118371"; bid=-KdjVq_c2QM; _vwo_uuid_v2=D424C0E7102A5AE5E76A787B5DBB3D0' \
             'EA|ac7fb1fcfcd42f19a81528a60c1ed77d; gr_user_id=5c53f769-b456-498c-8b14-f2e' \
             '8541f985d; viewed="30317874"; __yadk_uid=fyXblwL04jKPgWMleWOycMJ8stUdCM0G; ' \
             '_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1552462260%2C%22https%3A%2F%2Fwww.bai' \
             'du.com%2Flink%3Furl%3DSpQXmDjVlhxrW-SfhuSIpylG7eQ6fJ25eVe9YhCZsLK%26wd%3D%26' \
             'eqid%3De465fa6a000ab5bd000000065c88b1c1%22%5D; _pk_ses.100001.8cb4=*; __utma=3' \
             '0149280.741869300.1535465499.1552382223.1552462265.5; __utmc=30149280; __utmz=30' \
             '149280.1552462265.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbc' \
             'l2="193299191:Z0uoX7tsB54"; ck=_jR9; ap_v=0,6.0; push_noty_num=0; push_doumail_nu' \
             'm=0; __utmv=30149280.19329; _pk_id.100001.8cb4=bd91bcf9b7b44c1b.1535465494.4.15' \
             '52462360.1552382238.; __utmb=30149280.8.9.1552462361186'
    cookies = cookie_parse(cookie)   # 将cookie搞成字典样式的数据(键值对)
    denglu(cookies)



