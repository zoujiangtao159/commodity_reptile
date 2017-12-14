import traceback
import pickle
import requests
from bs4 import BeautifulSoup
import random


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

'''
# 定义要创建的目录
mkpath = "d:\\qttc\\web\\"
# 调用函数
mkdir(mkpath)
'''

def save_to_file(file_name, contents):
    fh = open(file_name,'w',encoding='utf-8')
    fh.write(contents)
    fh.close()



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
    shipping = soup.select('#attr-shipping > li')
    print(condition,shipping)
    print(specs)
    print(features)

    print(pictures)
    price = prices[0].get_text()
    print(price)
    title = titles[0].get_text()
    print(title)


def climb_category():
    climb_url = 'https://www.woot.com/'
    climb_s = requests.session()
    climb_rep = climb_s.get(climb_url)
    climb_req_result = climb_rep.content.decode(encoding='utf-8')
    climb_soup = BeautifulSoup(climb_req_result, 'lxml')
    #divs = climb_soup.find(class_='with-promo').find_all('div')
    titles = climb_soup.select('#global-header > div > nav.categories.with-promo > div > a > span')
    titles_url = climb_soup.select('#global-header > div > nav.categories.with-promo > div > a')
    climb_category_results = []
    for (title,title_url) in zip (titles,titles_url):
        category_result = {}
        url_result = title_url.get('href')
        title_result = title.get_text()
        #print(title_result,url_result)
        category_result['title'] = title_result
        category_result['url_result'] = url_result
        climb_category_results.append(category_result)
        #mkpath = "d:\\qttc\\web\\"+title_result
        # 调用函数
        #mkdir(mkpath)
    #print(climb_category_result)

    return climb_category_results


def climb_cat_type(climb_category_url):
    climb_cat_s = requests.session()
    climb_cat_rep = climb_cat_s.get(climb_category_url)
    climb_cat_req_result = climb_cat_rep.content.decode(encoding='utf-8')
    climb_cat_soup = BeautifulSoup(climb_cat_req_result, 'lxml')
    cat_type = climb_cat_soup.select('#content > div.ui-subcategory-grid-container > div.ui-subcategory-sub-header > a')
    if cat_type == []:
        cat_type_result = None
        cat_type_resulturl = None
    else:
        cat_type_result = cat_type[0].get('href')
        cat_type_resulturl = 'https://www.woot.com' + str(cat_type_result)
    return cat_type_resulturl


def climb_class(climb_category_results):
    climb_class_s = requests.session()
    print(climb_category_results['climb_cat_type_url'])
    climb_class_rep = climb_class_s.get(climb_category_results['climb_cat_type_url'])
    climb_class_rep_result = climb_class_rep.content.decode(encoding='utf-8')
    climb_class_soup = BeautifulSoup(climb_class_rep_result, 'lxml')
    climb_class_type_url_location = climb_class_soup.select('#content > div.content-wrapper > div.filter-list > ul > li > a')
    climb_class_type_title_location = climb_class_soup.select('#content > div.content-wrapper > div.filter-list > ul > li > a > span.title')
    class_list = []
    for  (climb_class_type_url_location_one,climb_class_type_title_one) in zip(climb_class_type_url_location,climb_class_type_title_location):
        climb_class_result = {}
        climb_class_type_url = climb_class_type_url_location_one.get('href')
        climb_class_type_title = climb_class_type_title_one.get_text()
        climb_class_result['class_title'] = climb_class_type_title
        climb_class_result['class_url'] = ['https://www.woot.com'+climb_class_type_url]
        class_list.append(climb_class_result)
        #mkpath = "d:\\qttc\\web\\"+climb_category_result['title']+"\\"+climb_class_type_title
        # 调用函数
        #mkdir(mkpath)
    return class_list



def climb_commodity_url(climb_category_result):

    climb_commodity_s = requests.session()
    #print(climb_category_results['climb_cat_type_url'])
    for  class_res in climb_category_result['climb_class_result']:
        class_res['commodity'] = []
        for class_url_one in class_res['class_url']:
            climb_commodity_get = climb_commodity_s.get(class_url_one)
            climb_commodity_get_rep_result = climb_commodity_get.content.decode(encoding='utf-8')
            climb_commodity_get_rep_result_soup = BeautifulSoup(climb_commodity_get_rep_result, 'lxml')
            commodity_url = climb_commodity_get_rep_result_soup.select('#content > div.content-wrapper > ul > li > a')
            commodity_title = climb_commodity_get_rep_result_soup.select(
                '#content > div.content-wrapper > ul > li > a > span.title ')
            commodity_next = climb_commodity_get_rep_result_soup.select(
                '#content > div.content-wrapper > div.pagination > ul > li > a.next')
            if commodity_next != []:
                for li_one in commodity_next:
                    # print(li_one.get('class'))
                    if li_one.get('class') == ['next']:
                        next_page_url = li_one.get('href')
                        class_res['class_url'].append('https://www.woot.com'+next_page_url)
                        #print(next_page_url)
            # print(commodity_title)
            class_res_ret_list = []
            for (commodity_url_one, commodity_title_one) in zip(commodity_url, commodity_title):
                class_res_ret = {}
                commodity_url_one_1 = commodity_url_one.get('href')
                # print(commodity_title_one)
                commodity_title_one_1 = commodity_title_one.get_text()
                class_res_ret['commodity_url'] = commodity_url_one_1
                class_res_ret['commodity_title'] = commodity_title_one_1
                mkpath = "d:\\qttc\\web\\"+climb_category_result['title']+"\\"+class_res['class_title']+"\\"+commodity_title_one_1.replace(' ','_').replace('"','').replace('?','').replace('?','').replace(':','').replace('.','').replace(',','').replace('-','').replace('\'','').replace('/','_').replace('\\','_')
                mkdir(mkpath)
                #print(climb_category_result)
                class_res_ret_list.append(class_res_ret)
            class_res['commodity'].append(class_res_ret_list)


if __name__ == '__main__':
    #reptile()
    climb_category_results = climb_category()
    for climb_category_result in climb_category_results:
        #print(climb_category_result['url_result'])
        climb_cat_type_result = climb_cat_type(climb_category_result['url_result'])
        climb_category_result['climb_cat_type_url'] = climb_cat_type_result
        if climb_cat_type_result != None:
            climb_class_rr =climb_class(climb_category_result)
            climb_category_result['climb_class_result'] = climb_class_rr
            climb_commodity_url(climb_category_result)
    print(climb_category_results)
    try:
        save_to_file('d:\\qttc\\web\\mobiles.txt', str(climb_category_results))
    except Exception as e:
        traceback.print_exc()
