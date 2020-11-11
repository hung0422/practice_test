import requests
from bs4 import BeautifulSoup

url = 'https://www.travel.taipei/zh-tw/tour/hellotaipei'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res = ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

title = soup.select('div[class="p-5 text-white z-100 hello-header-intro"]')[0].text
print(title)

'''
title2 = soup.select('div[class="max-width-xl mx-auto row"]')
for i in title2:
    test2 = i.select('p')
    for o in test2:
        print(o.text)
    '''

title2 = soup.select('div[class="max-width-xl mx-auto row"]')[0]
test = title2.select('div[class="hello-card-1 text-dark"]')
for i in test:
    test2 = i.select('p')
    for o in test2:
        print(o.text)
    print('')


title3 = soup.select('section[class="hello-traffic pb-7"]')[0]
train = title3.select('div[class="text-center text-dark pt-9 mb-3"]')[0].text
print(train)
train_text = title3.select('div[class="p-3 text-dark"]')
for i in train_text:
    print(i.text)



