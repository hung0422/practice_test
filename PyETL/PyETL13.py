import requests
from bs4 import BeautifulSoup

url = 'https://www.taiwan.net.tw/m1.aspx?sNo=0000108&jid=840'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res = ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

title = soup.select('div[class="right-side"]')[0].text
print(title)

'''
table = soup.select('article[class="tourArticle"]')
for i in table:
    print(i.text)
'''


table = soup.select('article[class="tourArticle"]')
for i in table:
    day = i.select('div[class="tourline1"]')
    day_text = i.select('div[class="tourlineSpots"]')
    for o in day:
        print(o.text)
        for p in day_text:
            print(p.text)