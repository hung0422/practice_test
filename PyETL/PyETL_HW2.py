from selenium.webdriver import Chrome  #104網站用requests無法抓到資料,所以改用這個
from bs4 import BeautifulSoup
import time
import os
import glob
import pandas as pd
import openpyxl   #原本用pandas無法存到excel,所以下載這模組,可是好像不用載入?

#創建資料夾
folder = './PyETLHomeWork2'
if not os.path.exists(folder):
    os.mkdir(folder)

#開啟104網站
driver = Chrome('./chromedriver')
url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E5%A4%A7%E6%95%B8%E6%93%9A&jobcatExpansionType=0&jobsource=2018indexpoc'


driver.get(url)
soup = BeautifulSoup(driver.page_source,'html.parser')

#104置頂的搜尋結果
title = soup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item js-job-item--focus b-block--ad"]')
for i in title:
    title2 = i.select('a')[0].text
    print(title2)
    url2 = 'https:' + i.select('a')[0]['href']
    print(url2)

    #進入文章裡
    driver.get(url2)

    #有時候網站頁面和python速度不同步就發生錯誤,或找不到資料,讓python休息一下
    time.sleep(2)
    #driver.implicitly_wait(2)

    #找資料
    soup2 = BeautifulSoup(driver.page_source, 'html.parser')

    company = soup2.select('a[data-v-4512f555]')[-1].text
    #print(company)
    job = soup2.select('h1[data-v-e9e2feee]')[0]['title']
    #print(job)
    content = soup2.select('p[data-v-6f6e08c2]')[0].text
    #print(content)
    require = soup2.select('div[class="job-requirement-table row"]')[0].text
    #print(require)
    welfare = soup2.select('p[data-v-d31d0296]')[0].text
    #print(welfare)
    contact = soup2.select('div[data-v-d919c298]')[2].text
    #print(contact)
    #print(url2)
    tool_all = soup2.select('u[data-v-65046123]')
    tool_list = [i.text for i in tool_all]
    tool = ','.join(tool_list)
    #print(tool)

    writein = 'company: {}---'.format(company)
    writein += 'job: {}---'.format(job)
    writein += 'content: {}---'.format(content)
    writein += 'requite: {}---'.format(require)
    writein += 'welfare: {}---'.format(welfare)
    writein += 'contact: {}---'.format(contact)
    writein += 'url: {}---'.format(url2)
    writein += 'tool: {}---'.format(tool)

    #存到txt檔
    try:
        with open('{}/{}.txt'.format(folder,title2),'w',encoding='utf-8') as f:
            f.write(writein)
    except :
        pass

    #回到上一頁
    driver.back()
    print('========================')

#104一般的搜尋結果
title3 = soup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')
for i in title3:
    title4 = i.select('a')[0].text
    print(title4)
    url3 = 'https:' + i.select('a')[0]['href']
    print(url3)

    # 進入文章裡
    driver.get(url3)

    # 有時候網站頁面和python速度不同步就發生錯誤,或找不到資料,讓python休息一下
    time.sleep(2)
    # driver.implicitly_wait(2)

    # 找資料
    soup3 = BeautifulSoup(driver.page_source,'html.parser')

    company = soup3.select('a[data-v-4512f555]')[-1].text
    #print(company)
    job = soup3.select('h1[data-v-e9e2feee]')[0]['title']
    #print(job)
    content = soup3.select('p[data-v-6f6e08c2]')[0].text
    #print(content)
    require = soup3.select('div[class="job-requirement-table row"]')[0].text
    #print(require)
    welfare = soup3.select('p[data-v-d31d0296]')[0].text
    #print(welfare)
    contact = soup3.select('div[data-v-d919c298]')[2].text
    #print(contact)
    #print(url3)
    tool_all = soup3.select('u[data-v-65046123]')
    tool_list = [i.text for i in tool_all]
    tool = ','.join(tool_list)

    #print(tool)

    writein = 'company: {}---'.format(company)
    writein += 'job: {}---'.format(job)
    writein += 'content: {}---'.format(content)
    writein += 'requite: {}---'.format(require)
    writein += 'welfare: {}---'.format(welfare)
    writein += 'contact: {}---'.format(contact)
    writein += 'url: {}---'.format(url3)
    writein += 'tool: {}---'.format(tool)

    #存到txt檔
    try:
        with open('{}/{}.txt'.format(folder,title4),'w',encoding='utf-8') as f:
            f.write(writein)
    except :
        pass

    #回到上一頁
    driver.back()
    print('=========================')

#關閉瀏覽器
driver.close()

#glob + pandas
file = glob.glob('./PyETLHomeWork2/*.txt')

data = list()
for i in file:
    with open(i,'r',encoding='utf-8') as f:
        file_a = f.read()
        file_b = [o for o in file_a.split('---') if o != '']
        data.append(file_b)

columns = [i.split(':')[0] for i in data[0]]

df = pd.DataFrame(data=data,columns=columns)

for col in columns:
    df[col] = df[col].apply(lambda x : x.split(':',1)[1])

#存到csv檔
#df.to_csv('test.csv',encoding='utf-8')

#存到execl檔
df.to_excel('HOMEWORK.xlsx',sheet_name='HOMEWORK',index=False)

