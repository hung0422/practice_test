import requests
#from bs4 import BeautifulSoup
import json
import os


keyword = str(input('關鍵字:'))
page = str(input('頁數:'))

#創建資料夾
folder = './104{}'.format(keyword)
if not os.path.exists(folder):
    os.mkdir(folder)

#設定迴圈頁數
for i in range(1,int(page)+1):
    #Crtl+U
    url = 'https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword={}&jobcatExpansionType=0&order=15&asc=0&page={}&mode=s&jobsource=2018indexpoc'.format(keyword,i)
    #設定104的headers
    headers = {"Referer": "https://www.104.com.tw/job/ajax/content/6p2d6",}

    ss = requests.session()
    res = ss.get(url=url,headers=headers)
    #soup = BeautifulSoup(res.text,'html.parser')
    #json格式
    a = json.loads(res.text)

    data = a['data']
    list = data['list']
    #找頁面網址
    for i in list:
        url_tmp = i['link']['job']
        url_tmp2 = url_tmp.split('?')[0]
        url_tmp3 = 'https:' + url_tmp2.split('job')[0]+'job/ajax/content'
        url_tmp4 = url_tmp2.split('job')[1]
        url_after = url_tmp3+url_tmp4
        print(url_after)

        #進入頁面
        res_after = ss.get(url=url_after, headers=headers)

        require = '接受身分：'
        contact = '聯絡人:'

        #json格式+找資料
        b = json.loads(res_after.text)

        data = b['data']
        data1 = data['header']
        company = data1['custName']
        # print(company)
        job = data1['jobName']
        # print(job)
        detail = data['jobDetail']
        # print(detail)
        content = detail['jobDescription']
        # print(content)
        condition = data['condition']
        condition2 = condition['acceptRole']['role']
        for i in condition2:
            require += (i['description'] + '，')

        workexp = condition['workExp']
        edu = condition['edu']
        major = condition['major']

        require += '工作經歷:{}  '.format(workexp)
        require += '學歷要求:{}  科系要求:'.format(edu)

        for i in major:
            require += '{} '.format(i)
        require += '語文條件:'
        language = condition['language']

        for i in language:
            for o in i:
                require += i[o] + ' '

        other = condition['other']
        require += '其他條件:{}'.format(other)
        # print(require)

        contact_text = data['contact']

        contact += contact_text['hrName']
        contact += ' E-mail:{}'.format(contact_text['email'])
        # print(contact)

        tool = ''
        specialty = condition['specialty']
        for i in specialty:
            tool += i['description'] + ' '
        # print(tool)

        welfare = data['welfare']['welfare']
        # rint(welfare)

        writein = 'company: {}---'.format(company)
        writein += 'job: {}---'.format(job)
        writein += 'content: {}---'.format(content)
        writein += 'requite: {}---'.format(require)
        writein += 'welfare: {}---'.format(welfare)
        writein += 'contact: {}---'.format(contact)
        writein += 'url: {} ---'.format(url_after)
        writein += 'tool: {}---'.format(tool)

        #print(writein)
        #寫入檔案
        try:
            with open('{}/{}.txt'.format(folder,company),'w',encoding='utf-8') as f:
                f.write(writein)
        except:
            pass

