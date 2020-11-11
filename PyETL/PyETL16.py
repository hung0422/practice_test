import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import os



#url = 'https://travel.yahoo.com.tw/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
#res = ss.get(url=url,headers=headers)
#soup = BeautifulSoup(res.text,'html.parser')

page = str(input('第幾頁:'))
keyword = str(input('輸入要搜尋的詞:'))
'''
data = {'P': page,
        'T': keyword,
        'type': 'search',
        'GATitle': '關鍵字搜尋'}
'''
url_after = 'https://travel.yahoo.com.tw/ajax/LoadMore.php'
#print(url_after)

for nu_page in range(1,int(page)+1):

    data = {'P': nu_page,
            'T': keyword,
            'type': 'search',
            'GATitle': '關鍵字搜尋'}


    res_after = ss.post(url_after,data=data,headers=headers)

    soup_after = BeautifulSoup(res_after.text,'html.parser')
    title = soup_after.select('div[class="item_topic dotdotdot"]')
    title2 = soup_after.select('div[class="item_desc dotdotdot"]')
    title_url = soup_after.select('a[href]')
    for i in range(len(title)):
        print(title[i].text)
        print(title2[i].text)
        href = title_url[i]['href']
        href_tran = quote(href)
        title_url2 = 'https://travel.yahoo.com.tw' + href_tran
        print(title_url2)


        res_after2 = ss.get(url=title_url2, headers=headers)
        soup = BeautifulSoup(res_after2.text, 'html.parser')

        content = soup.select('h1[class="post_title"]')[0].text
        print(content)
        content2 = soup.select('p[class="date"]')[0].text
        print(content2)

        content3 = soup.select('div[class="post_content"]')
        for i in content3:
            print(i.text)




