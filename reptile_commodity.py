import requests
from bs4 import BeautifulSoup
import random


def reptile():
    url = 'https://computers.woot.com/offers/hp-omen-870-i7-32gb-ddr4-radeon-rx480-desktop-17?ref=w_cnt_lnd_cat_pc_3_10'
    s = requests.session()
    data = s.get(url)
    req_result = data.content.decode(encoding='utf-8')
    soup = BeautifulSoup(req_result,'lxml')
    titles = soup.select('#attribute-selector > header > h1') #抬头
    prices = soup.select('#attribute-selector > div.price-exact > span')#价格
    pictures = soup.select('#gallery')#图片
    features = soup.select('#tab-features > article > ul')#特征
    specs = soup.select('#tab-specs')#描述
    condition = soup.select('#attr-condition')#条件
    print(specs)
    print(features)
    print(pictures)
    print(prices)
    print(titles)
    for i in range(3):
        print(random.randint(0,9))




if __name__ == '__main__':
    reptile()