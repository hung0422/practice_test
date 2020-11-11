import requests
from bs4 import BeautifulSoup

url = 'https://tour.settour.com.tw/product/GFG0000014382?cmsCode=IDX-E05C-01&ds=3&a=ADV0000000312&s=5901'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss =requests.session()
res = ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

title = soup.select('h1[class="product-in-tit"]')[0].text
print(title)
print(' ')

title2 = soup.select('div[class="editor-area"]')[0].text
title3 = title2.split('更多')[0]
print(title3)
print(' ')

paper = soup.select('div[class="stroke-item-tit-stroke"]')
paper2 = soup.select('div[class="stroke-item-info-text"]')
paper3 = soup.select('div[class="stroke-item-tit-day"]')
for i in range(len(paper)):
    print(paper3[i].text)
    print(paper[i].text)
    print(paper2[i].text)
    print(' ')
print(' ')

title4 = soup.select('div[class="editor-area"]')[1].text
title5 = title4.split('註1')[0]
print(title5)
print(' ')