from bs4 import BeautifulSoup
import requests
import pymysql
import pickle

Count=0

def read_cookies():
    try:
        with open('cookies.txt', 'rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
        return cookies
    except Exception as e:
        print (e)
        return None

def get_ebaycom(userid,data=None):
    headers = {
        'Referer': 'http://music.163.com/',
        'Host': 'music.163.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://music.163.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
    }
    url = 'http://music.163.com/user/home?id='+ str(userid)
    cookies = read_cookies()
    proxies = {"http": '111.13.2.131:80'}
    s = requests.session()
    #print(url,cookies,headers)
    wb_data = s.get(url, cookies=cookies, headers=headers,proxies=proxies)
    result_res = wb_data.content.decode(encoding='utf-8')
    #print('----------------------\n',result_res)
    soup = BeautifulSoup(result_res,'lxml')
    #print(soup)
    titles = soup.select('#head-box > dd > div.inf.s-fc3.f-cb > ul')
    print(titles)
    xingbie = soup.select('#j-name-wrap > i')
    xingbie_1  = xingbie[0].get('class')
    print(xingbie_1[2])
    if  'u-icn-02' in xingbie_1:
        print('888888'*10)
    imgs = soup.select('#rHeader > h4')
    print('-------------------------',imgs)
    dess = soup.select('#m-record')
    number = dess[0].get('data-songs')
    if int(number) >1000:
        print(userid,'听歌数量为',number)
        listen_song_number(userid,number)


conn = pymysql.connect(host='localhost',user='root', passwd='qwer@1234', db='bdm252107406_db', use_unicode=True,charset="utf8")

def deffent_source():
    cursor = conn.cursor()
    sql2 = ('SELECT DISTINCT source FROM result')
    cursor.execute(sql2)
    qw1 = cursor.fetchall()
    return qw1

def listen_song_number(userid,number):
    cursor = conn.cursor()
    sql = 'insert into listen_song_number values(%d,%d)' % (int(userid), int(number))
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
        pass
    conn.commit()


if __name__ == '__main__':
    source_id =deffent_source()
    for user_source_id in source_id:
        print(user_source_id[0])
        get_ebaycom(user_source_id[0])