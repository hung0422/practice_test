import requests
from bs4 import BeautifulSoup

url = 'https://travel.yahoo.com.tw/%E5%8C%97%E6%B5%B7%E9%81%93%E6%97%85%E9%81%8A%E5%B0%B1%E8%A6%81%E5%90%83%E8%9E%83%E8%9F%B9-%E6%9C%AD%E5%B9%8C5%E9%96%93%E8%9E%83%E8%9F%B9%E7%BE%8E%E9%A3%9F%E9%A4%90%E5%BB%B3%E5%A4%A7%E9%9B%86%E5%90%88-043000992.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res = ss.get(url=url,headers=headers)
soup = BeautifulSoup(res.text,'html.parser')


title = soup.select('h1[class="post_title"]')[0].text
print(title)
title2 = soup.select('p[class="date"]')[0].text
print(title2)

title3 = soup.select('div[class="post_content"]')
for i in title3:
    print(i.text)

