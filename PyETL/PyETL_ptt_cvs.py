import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import glob
import time

#創建資料夾
folder = './ptt_CVS'
if not os.path.exists(folder):
    os.mkdir(folder)

url = 'https://www.ptt.cc/bbs/CVS/index.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}


page = int(input('頁數:'))
#找資料+存檔
for i in range(page):
    ss = requests.session()
    res = ss.get(url=url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    paper = soup.select('div[class="title"]')
    for paper3 in paper:
        try:
            paper2 = paper3.select('a')[0].text
            print(paper2)

            url2 = 'https://www.ptt.cc' + paper3.select('a')[0]['href']
            print(url2)

            res2 = ss.get(url=url2,headers=headers)

            soup2 = BeautifulSoup(res2.text,'html.parser')

            essay = soup2.select('div[id="main-content"]')[0]
            essay2 = essay.text.split('--')[0]

            good = 0
            bed = 0
            normal = 0

            essay3 = essay.select('div[class="push"]')
            for push in essay3:
                total = push.text.split(' ')[0]
                if total == '推':
                    good += 1
                elif total == '噓':
                    bed += 1
                elif total == '→':
                    normal += 1

            finial = soup2.select('span[class="article-meta-value"]')

            author = finial[0].text
            title = finial[2].text
            period = finial[3].text

            message_total = ''

            message_all = soup2.select('div[class="push"]')
            for message in message_all:
                try:
                    message_push = message.select('span[class="f1 hl push-tag"]')[0].text
                except IndexError:
                    message_push = message.select('span[class="hl push-tag"]')[0].text
                message_author = message.select('span[class="f3 hl push-userid"]')[0].text
                message_concent = message_push + message_author + message.select('span[class="f3 push-content"]')[0].text
                message_total += message_concent + '\n'

            writein = essay2
            writein += '\n---message---\n'
            writein += message_total
            writein += '\n---split---\n'
            writein += '推: {}\n'.format(good)
            writein += '噓: {}\n'.format(bed)
            writein += '一般: {}\n'.format(normal)
            writein += '分數: {}\n'.format(good-bed)
            writein += '作者: {}\n'.format(author)
            writein += '標題: {}\n'.format(title)
            writein += '時間: {}\n'.format(period)

            if not os.path.exists('{}/{}.txt'.format(folder, paper2)):
                with open('{}/{}.txt'.format(folder, paper2), 'w', encoding='utf-8') as f:
                    f.write(writein)
            else:
                with open('{}/{}.txt'.format(folder, paper2 + str(1)), 'w', encoding='utf-8') as f:
                    f.write(writein)

        except IndexError:
            pass
    url3 = soup.select('div[class="btn-group btn-group-paging"]')[0]
    url = 'https://www.ptt.cc' + url3.select('a[class="btn wide"]')[1]['href']

    if i % 20 == 0:
        time.sleep(5)

#glob + pandas
fileall = glob.glob('./ptt_CVS/*.txt')

data = list()
for file in fileall:
    with open(file,'r',encoding='utf-8') as f:
        file_a = f.read()
        file_b = file_a.split('---split---')[1]
        file_c = [i for i in file_b.split('\n') if i != '']
        data.append(file_c)

columns = [i.split(':')[0] for i in data[0]]
df = pd.DataFrame(data=data,columns=columns)

for col in columns:
    df[col] = df[col].apply(lambda x :x.split(':')[1])

df.to_excel('ptt_CVS_pandas.xlsx',encoding='utf-8')