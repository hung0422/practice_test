import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import glob
import time




headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}


#找資料+存檔

ss = requests.session()





url2 = 'https://www.ptt.cc/bbs/CVS/M.1597200881.A.3A7.html'
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
    message_total += message_concent+'\n'

    #print(message_concent)

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

print(writein)