import requests
import json
import time
import os

folder_num = 0

ss = requests.session()

keyword = str(input('關鍵字:'))
#創建資料夾
keyword_folder = './{}'.format('KKday'+keyword)
if not os.path.exists(keyword_folder):
    os.mkdir(keyword_folder)

#設定換頁參數
qqq = 1
www = 0

headers = {
        'referer': 'https://www.kkday.com/zh-tw/product/30',
        'cookie': 'currency=TWD; CID=5704; KKUD=1f5586b75b2753fc40e16b0b78fb0653; _gcl_au=1.1.2098010905.1596683177; country_lang=zh-tw; case_id=8; _ga=GA1.2.373895176.1596683178; _hjid=cf00a24f-6526-44c0-9f5f-412b2ae83b9a; __lt__cid=7d942561-4042-4c64-88f9-d008b160ea03; adid=159668318056184; _fw_crm_v=b1a36886-cdbc-4136-dd57-c972ce9cfba9; recent_search=%5B%22A01-001-00001%22%2C%22A01-001-00008%22%5D; csrf_cookie_name=1985f0334072ff799108c32138c4f4ad; __lt__sid=de5a8729-125daea8; _gid=GA1.2.1198570701.1596975667; mp_b8150a8ddf736c19fdc0f146b9ffac24_mixpanel=%7B%22distinct_id%22%3A%20%22173c1bbcf0961f-01c05124dc65b3-b7a1334-144000-173c1bbcf0a604%22%2C%22%24device_id%22%3A%20%22173c1bbcf0961f-01c05124dc65b3-b7a1334-144000-173c1bbcf0a604%22%2C%22Platform%22%3A%20%22www.kkday.com%22%2C%22LoginChannel%22%3A%20%22NO%22%2C%22DisplayCurrency%22%3A%20%22TWD%22%2C%22DisplayLang%22%3A%20%22zh-tw%22%2C%22DisplayCountry%22%3A%20%22TW%22%2C%22IsInternal%22%3A%20false%2C%22Cid%22%3A%20%225704%22%2C%22Ud1%22%3A%20null%2C%22Ud2%22%3A%20null%2C%22%24'
    }

#換頁迴圈
while qqq != www:

    url = 'https://www.kkday.com/zh-tw/product/ajax_productlist/A01-001?country=A01-001&city=A01-001-00001&keyword={}&time=&glang=&sort=prec&page={}&row=10&fprice=*&eprice=*&precurrency=TWD&csrf_token_name=1985f0334072ff799108c32138c4f4ad'.format(keyword,qqq)

    res = ss.get(url=url,headers=headers)
    b = json.loads(res.text)

    #print(b)
    total_page = b['total_page']
    #print(total_page)
    title_data = b['data']
    for i in title_data:
        folder_num += 1
        #print(i)
        title_name = i['name']
        #print(title_name)
        title_introduction = i['introduction']
        #print(title_introduction)
        total_score = i['rating_star']
        #print(total_score)
        people = i['rating_count']
        #print(people)
        title_url = i['url']
        print(title_url)
        enter_url1 = title_url.split('product/')[0]+'product/ajax_get_page_comments/'
        enter_url2 = title_url.split('product/')[1]
        #搜尋頁面網址
        enter_url = enter_url1 + enter_url2
        #print(enter_url)

        # 創建資料夾
        folder = '{}/{}'.format(keyword_folder, keyword + str(folder_num))
        if not os.path.exists(folder):
            os.mkdir(folder)

        #設定換頁參數
        ppp = 1

        zzz = 1
        xxx = 0

        #換頁迴圈
        while zzz != xxx:

            data = {'json[currentPage]': zzz,
                    'json[pageSize]': 10,
                    'csrf_token_name': '1985f0334072ff799108c32138c4f4ad'}

            ss = requests.session()
            res = ss.post(url=enter_url, data=data, headers=headers)
            # soup = BeautifulSoup(res.text,'html.parser')
            a = json.loads(res.text)

            #找留言
            for i in a:
                name = i['firstName']
                print(name)
                score = '★' * int(i['recScore']) + '☆' * (5-int(i['recScore']))
                print(score)
                comment_title = i['translatedRecTitle']
                print(comment_title)
                comment = i['recDesc']
                print(comment)
                comment_data = i['recDt']
                print(comment_data)

                writein = title_name + '\n' + title_introduction
                writein += '\n\n旅客評價: {}  {}則旅客評價'.format(total_score, people)
                writein += '\n---split---\n'
                writein += '旅客: {}\n'.format(name)
                writein += '分數: {}\n'.format(score)
                writein += '評論: {}\n{}\n'.format(comment_title,comment)
                writein += '時間: {}\n'.format(comment_data)

                print(writein)
                #轉json檔
                writein_json = json.dumps(writein)

                #寫進檔案裏
                if not os.path.exists('{}/{}.txt'.format(folder, name)):
                    with open('{}/{}.txt'.format(folder, name), 'w', encoding='utf-8') as f:
                        f.write(writein_json)
                else:
                    with open('{}/{}.txt'.format(folder, name + str(ppp)), 'w', encoding='utf-8') as f:
                        f.write(writein_json)
                        ppp += 1

            #自動換頁條件
            zzz += 1
            if len(a) != 10:
                xxx = zzz
            else:
                pass

            if zzz % 10 == 0:
                time.sleep(2)
    #自動換頁條件
    qqq += 1
    if len(title_data) != 10:
        qqq = www
    else:
        pass

    if qqq % 10 == 0:
        time.sleep(2)