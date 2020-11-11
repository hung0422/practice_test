import requests
from bs4 import BeautifulSoup
import json

url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=apple&limit=50&newest=0&order=desc&page_type=search&version=2'
headers = {
    'referer': 'https://shopee.tw/search?keyword=apple&page=2',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}


ss = requests.session()
res = ss.get(url=url,headers=headers)
a = json.loads(res.text)


title = a['items'][0]
#print(title)
title_id = title['itemid']
#print(title_id)
title_shopid = title['shopid']
#print(title_shopid)
title_name = title['name']
print(title_name)
title_url = 'https://shopee.tw/api/v2/item/get?itemid={}&shopid={}'.format(title_id,title_shopid)
#print(title_url)

res_after = ss.get(title_url,headers=headers)
b = json.loads((res_after.text))

print(b)
paper = b['item']['description']
print(paper)
price_min = b['item']['price_min']
print(price_min)