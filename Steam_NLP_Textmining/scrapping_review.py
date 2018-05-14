from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.request import urlopen
import time
import re
import numpy as np
import csv
######functions######
#get_text 달기
def idx_get_text(i,classes):
    class_text = classes[i].get_text()
    return class_text

#APP ID 추출 part
def extract_appid(num_of_page):
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)

    id_list = []
    for i in range(num_of_page):
        if (i + 1) == 1:
            url = 'https://steamdb.info/apps/'
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            game_id = soup.findAll("tr", {"data-appid": re.compile("[0-9]*")})  # ???

            for each_id in game_id:
                if each_id.find(class_='subinfo').get_text() == "Game":  # 게임 item의 id만 crawling (Unknown 등 제외)
                    id_list.append(each_id['data-appid'])
                else:
                    pass

        if (i + 1) != 1:
            url = 'https://steamdb.info/apps/page' + str(i)
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            game_id = soup.findAll("tr", {"data-appid": re.compile("[0-9]*")})

            for each_id in game_id:
                if each_id.find(class_='subinfo').get_text() == "Game":
                    id_list.append(each_id['data-appid'])
                else:
                    pass

    id_list = list(set(id_list))
    return id_list
## main code
if __name__ == "__main__":
    # for j in range(1,12):
    # appid_list = extract_appid(1164)
    appid_list =[]
    with open('id_list.csv','r',encoding='utf8') as f :
        appid = csv.reader(f)
        for j in appid:
            appid_list.append(j[0].replace(" ",''))

    driver = webdriver.Chrome()

    driver.implicitly_wait(3)
    #review 추출
    whole_id_review ={}
    for k , id in enumerate(appid_list[8952:]):
        main_url = "https://steamcommunity.com/app/"+id+"/reviews/"
        # print(main_url)
        driver.get(main_url)

        time.sleep(1)

        elem = driver.find_element_by_tag_name("body")
        pre_htmls= driver.page_source
        pre_soups = BeautifulSoup(pre_htmls, 'html.parser')
        pre_review = pre_soups.find_all("div",{"class": "apphub_CardTextContent"})

        # continue나올 경우 click처리
        try :
            if pre_soups.find('div', {'id': 'age_gate_btn_continue'}).get_text() == "\nContinue\n":
                button_continue = '//*[@id="age_gate_btn_continue"]'
                # // *[ @ id = "age_gate_btn_continue"]
                driver.find_element_by_xpath(button_continue).click()
                print("click is done!")
                time.sleep(3)
                elem = driver.find_element_by_tag_name("body")
                pre_htmls = driver.page_source
                pre_soups = BeautifulSoup(pre_htmls, 'html.parser')
                pre_review = pre_soups.find_all("div", {"class": "apphub_CardTextContent"})
            else :
                pass
        except AttributeError :
            # print('no continue button so.. go to next step!')
            pass

        if len(pre_review) != 0:     #review유무 판단
            for num in range(100) : #page down
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)

            time.sleep(3)

            if driver.current_url == main_url:
                htmls = driver.page_source
                soups = BeautifulSoup(htmls, 'html.parser')

                reviews = soups.find_all("div",{"class": "apphub_CardTextContent"})
                labels =  soups.find_all("div",{"class": "title"})

                reviews_list = []
                labels_list = []
                for i in range(len(reviews)):
                    reviews_list.append(idx_get_text(i,reviews).split('\n')[-1].replace('\t','').replace(',','')+"//")

                # print(reviews_list)
                for j in range(len(labels)):
                    labels_list.append(idx_get_text(j,labels))
                # print(labels_list)
                arr_reviews = np.array(reviews_list)
                arr_labels = np.array(labels_list)
                # print(arr_labels)
                arr_review_labels = np.core.defchararray.add(arr_reviews,arr_labels)
                review_label_list = arr_review_labels.tolist()
                whole_id_review[id] = review_label_list

                with open('steam_reviews.txt','a',encoding='utf8',newline='') as f:
                    w = csv.writer(f)
                    w.writerow([id]+whole_id_review[id])
                print("("+ str(k+1)+"/" + str(len(appid_list))+ ") "+ str(id) +" is completed!")

            else :
                print(str(id) + " can not get soups!!")

        else :
            print(str(id) +" has no reviews!")
    # whole_id_review_keys = sorted(whole_id_review.keys())
    # with open('steam_reviews_'+ str(100) +'.csv','w',encoding='utf8',newline='') as f:
    #     # w = csv.DictWriter(f,whole_id_review.keys())
    #     w = csv.writer(f)
    #     # w.writeheader()
    #     # w.writerows()
    #     for k,v in whole_id_review.items():
    #         w.writerow([k] + v)



