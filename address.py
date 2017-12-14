import json
import urllib

import requests



url = 'http://c.snnd.co/api/v4/click?campaign_id=5302677\u0026publisher_id=1491\u0026rt=171023035757\u0026_po=89ae56c1c07aa10f25a806964a09f263\u0026_mw=p\u0026_c=3000\u0026_cw=c\u0026_ad=111\u0026publisher_slot=5079_1002620\u0026sub_1=\u0026pub_gaid=1f0ba7e7-8520-48e1-9c7e-d4775f609ca9\u0026pub_idfa=\u0026pub_aid=df255b43ff8dbce0'
def get_final_url(hi_url):
    r = requests.get(hi_url,allow_redirects=False)
    try:
        jump_url = requests.head(url).headers['Location']
    except:
        jump_url = None
    print(jump_url)
    #print(r.url)
    return jump_url
wer = []
while url != None :
    url = get_final_url(url)