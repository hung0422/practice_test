from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import time
import os

keyword = str(input('輸入關鍵字:'))
folder_num = 0
#創建資料夾
keyword_folder = './{}'.format('KKday'+keyword)
if not os.path.exists(keyword_folder):
    os.mkdir(keyword_folder)


#開啟瀏覽器
driver = Chrome('./chromedriver')
url = 'https://www.kkday.com/zh-tw/'

driver.get(url)
time.sleep(3)

#輸入關鍵字及搜尋
driver.find_element_by_id('search_experience_value').send_keys(keyword)
driver.find_element_by_class_name('input-group-btn').click()
time.sleep(3)
#選擇別類中的觀光旅行
driver.find_element_by_xpath('//div[@value="TAG_4"]').click()
driver.find_element_by_xpath('//i[@class="fa fa-square-o fa-lg"]').click()
time.sleep(3)


soup = BeautifulSoup(driver.page_source,'html.parser')

#設定換頁參數
test = 5
b = '1'
num3 = 2

#換頁迴圈
while str(test) != str(num3) :
    #換頁參數
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    num = soup.select('ul[class="pagination"]')[0]
    num2 = num.select('li[class="a-page"]')
    num3 = num.select('li[class="a-page active"]')[0].text
    a = num2[-1].text


    catalog = soup.select('div[class="product-listview search-info"]')
    for i in catalog:
        catalog2 = i.select('a')
        folder_num +=1
        for o in catalog2:
            # 點連結進入
            driver.find_element_by_id(o['id']).click()
            time.sleep(4)
            # 獲得當前瀏覽器所有視窗
            windows = driver.window_handles
            # 切換到最新開啟視窗
            driver.switch_to_window(windows[-1])

            soup2 = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                # 找內容
                title = soup2.select('div[class="product-name"]')[0].text
                # print(title)
                title2 = soup2.select('div[id="prodInfo"]')[0]
                title3 = title2.select('p[class="pre-line"]')[0].text
                # print(title3)
                title4 = title2.select('ul')[-1].text
                # print(title4)

                content = soup2.select('div[class="new-product product-info-wrap"]')[0]
                content2 = content.select('p')[1].text
                # print(content2)



                #旅客總評分
                total_score = soup2.select('div[id="review-sec"]')[0]
                score = total_score.select('div[class="review-score"]')[0].text
                # print('評分:'+ score)

                # js="var q=document.documentElement.scrollTop=10000"
                # driver.execute_script(js)


                # 創建資料夾
                folder = '{}/{}'.format(keyword_folder,keyword+str(folder_num))
                if not os.path.exists(folder):
                    os.mkdir(folder)
                time.sleep(2)
                # 設定換頁參數
                test2 = 5
                bb = '1'
                num100 = 2
                zzz = 1


                # 找留言迴圈
                while str(test2) != str(num100):
                    # 參數
                    soup2 = BeautifulSoup(driver.page_source, 'html.parser')

                    num = soup2.select('ul[class="pagination"]')[0]
                    num2 = num.select('li[class="a-page"]')
                    num100 = num.select('li[class="a-page active"]')[0].text

                    a = num2[-1].text

                    #找留言
                    travel_comment = soup2.select('div[id="review-sec"]')[0]
                    travel_comment2 = travel_comment.select('div[class="review-item"]')
                    for i in travel_comment2:
                        star100 = i.select('svg[class="kk-icon star star-100"]')
                        star0 = i.select('svg[class="kk-icon star star-0"]')
                        star = '★' * len(star100) + '☆' * len(star0)
                        # print(star)
                        name = i.select('span[class="text-heavy"]')[0].text
                        # print(name)
                        comment = i.select('p')[0].text
                        # print(comment)
                        comment_time = i.select('div[class="review-info"]')[0].text.split(' ')[1]
                        # print(comment_time)

                        writein = title + '\n' + title3 + '\n' + title4 + '\n' + content2
                        writein += '\n\n旅客評價: {}'.format(score)
                        writein += '\n---split---\n'
                        writein += '旅客: {}\n'.format(name)
                        writein += '分數: {}\n'.format(star)
                        writein += '評論: {}\n'.format(comment)
                        writein += '時間: {}\n'.format(comment_time)

                        print(name)

                        # 寫進檔案裏
                        if not os.path.exists('{}/{}.txt'.format(folder,name)):
                            with open('{}/{}.txt'.format(folder,name),'w',encoding='utf-8') as f:
                                f.write(writein)
                        else:
                            with open('{}/{}.txt'.format(folder,name+str(zzz)),'w',encoding='utf-8') as f:
                                f.write(writein)
                            zzz += 1
                    # print(writein)

                    # 自動換頁
                    if num100 == '1':
                        test2 = 0
                    else:
                        try:
                            test2 = int(a) + int(bb)
                        except:
                            test2 = a + bb

                    if str(test2) == str(num100):
                        pass
                    else:
                        driver.find_element_by_link_text(str(int(num100) + 1)).click()

                    time.sleep(3)
            except:
                pass

            # 關閉當前視窗
            driver.close()
            time.sleep(2)
            # 切換到原本視窗
            driver.switch_to_window(windows[0])

    #自動換頁條件
    if num3 == '1':
        test = 0
    else:
        try:
            test = int(a) + int(b)
        except:
            test = a + b

    if str(test) == str(num3):
        pass
    else:
        driver.find_element_by_link_text(str(int(num3)+1)).click()

    time.sleep(4)
