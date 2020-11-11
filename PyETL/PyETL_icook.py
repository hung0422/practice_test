import requests
from bs4 import BeautifulSoup
import os
import time

url_all = 'https://icook.tw/categories?ref=breadcrumb-category'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
ss = requests.session()
res_all = ss.get(url=url_all,headers=headers)
soup_all = BeautifulSoup(res_all.text,'html.parser')

title_all = soup_all.select('ul[class="categories-all-content"]')[0]
title_all2 = title_all.select('li[class="categories-all-parents"]')
for title_all3 in title_all2:
    headline = title_all3.select('h6[class="categories-all-parent-name"]')[0]['id']

    #創建資料夾
    folder_icook = './icook'
    if not os.path.exists(folder_icook):
        os.mkdir(folder_icook)

    # 創建資料夾
    folder_headline = '{}/{}'.format(folder_icook,headline)
    if not os.path.exists(folder_headline):
        os.mkdir(folder_headline)

    subtitle = title_all3.select('ul[class="categories-all-children"]')
    for subtitle2 in subtitle:
        title = subtitle2.select('a[class="categories-all-child-link"]')
        for i in title:
            title2 = i['name']
            title_url = 'https://icook.tw/' + i['href']

            #設定迴圈 & 進入中標題
            page = 1
            test_page = 0

            while page != test_page:
                title_url2 = title_url + '?page={}'.format(page)

                title_res = ss.get(url=title_url, headers=headers)
                title_soup = BeautifulSoup(title_res.text, 'html.parser')

                writein = ''

                food_all = title_soup.select('a[class="browse-recipe-link"]')
                for food_all2 in food_all:
                    food_all3 = food_all2.select('div[class="browse-recipe-preview"]')[0]
                    food_title = food_all3.select('span')[0]['title']
                    food_url = 'https://icook.tw/' + food_all2['href']
                    #食譜名稱
                    print(food_title)
                    #食譜網址
                    print(food_url)

                    '''
                    if not os.path.exists('{}/{}.txt'.format(folder_headline,title2)):
                        with open('{}/{}.txt'.format(folder_headline,title2),'w',encoding='utf-8') as file:
                            file.write(writein)
                    '''


                page += 1
                if len(food_all) != 18:
                    test_page = page
                else:
                    pass

                if test_page % 10 == 0:
                    time.sleep(10)
