import requests
from bs4 import BeautifulSoup
import json

url = 'https://api.cnyes.com/media/api/v1/newslist/category/headline?limit=30&startAt=1596297600&endAt=1597247999&page=2'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res = ss.get(url=url,headers=headers)
a = json.loads(res.text)


json_a = a['items']['data'][0]
title_id = json_a['newsId']
title = json_a['title']
print(title)
url_after = 'https://news.cnyes.com/news/id/' +str(title_id) +'?exp=a'

res_after = ss.get(url=url_after,headers=headers)
soup = BeautifulSoup(res_after.text,'html.parser')

time_data = soup.select('div[class="_1R6L"]')[0].text
print(time_data.split('face')[0])

paper = soup.select('section[class="_82F6"]')[0].text
print(paper)