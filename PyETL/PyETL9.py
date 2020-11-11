import requests
from bs4 import BeautifulSoup

url = 'https://www.taiwan.net.tw/m1.aspx?sNo=0001016&id=19'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res = ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

title = soup.select('div[class="content"]')[0]
title2 = title.select('div[class="wrap"]')[0]
title3 = title2.select('p')

for i in range(len(title3)):
    if i >4:
        pass
    else:
        print(title3[i].text)