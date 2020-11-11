import requests
from bs4 import BeautifulSoup

url = 'https://trip.eztravel.com.tw/domestic/introduction/GRT0000009109?depDateFrom=&depDateTo=&avaliableOnly=false'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res = ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

#title = soup.select('div[class="product-info css-td"]')[0].text
#print(title)

stroke = soup.select('li[class="day-list"]')
for i in stroke:
    day = i.select('div[class="title-circle title-circle-green nth-day"]')
    day_title = i.select('div[class="day-box"]')
    day_time = i.select('div[class="intro-time"]')
    day_text = i.select('div[class="intro-content"]')
    for d in range(len(day_title)):
        print(day[0].text)
        print(day_title[0].text)
        for o in range(len(day_time)):
            print(day_time[o].text)
            print(day_text[o].text)
