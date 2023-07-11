from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

#기본 비어있는 리스트를 만듬. 여기에 값들을 저장할 예정
li_task = []
li_title = []
li_notice = []
li_demand = []



#총 10페이지까지(1페이지에 10개, 10*10 100개를 크롤링할 예정)할 예정이라 for 문 돌림
#이때 url을 살펴보면 페이지 넘버에 따라 뒤 숫자가 바뀌는 유형이었음. 만약에 페이지 넘버가 안바뀐다면? selenium의 click매소드를  활용해서 계속 페이지를 넘겨줬을 예정
for i in range(1, 31):
    url = f'https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?area=&bidNm=%B0%F8%B0%A3%C1%A4%BA%B8&bidSearchType=1&fromBidDt=2023%2F01%2F07&fromOpenBidDt=&instNm=&maxPageViewNoByWshan=2&radOrgan=1&regYn=Y&searchDtType=1&searchType=1&taskClCds=&toBidDt=2023%2F07%2F10&toOpenBidDt=&currentPageNo={i}'

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find_all('tbody') #tbody에 id나 class 정의가 없었음. 딱 1개여서.
    infos = contents[0].find_all('tr')

    for info in infos: #10개의 infos를 하나씩 분리하는 과정. 내가 필요한 것만 뽑았음. 다른것도 뽑을 수 있음
        task = info.select_one('td:nth-of-type(1)').text #업무 추출

        if task == '용역':
            title = info.select_one('td:nth-of-type(4)').text #공고명
            notice = info.select_one('td:nth-of-type(5)').text #공고기관
            demand = info.select_one('td:nth-of-type(6)').text #수요기관
            li_task.append(task) #빈 리스트에 업무 하나씩 넣기
            li_title.append(title) #빈 리스트에 공고명 하나씩 넣기
            li_notice.append(notice)#빈 리스트에 공고기관 하나씩 넣기
            li_demand.append(demand) #빈 리스트에 수요기관 하나씩 넣기
        else:
            break

        
    



    
#끝났으니까 csv로 추출하기.
df = pd.DataFrame({
    '업무': li_task,
    '공고명': li_title,
    '공고기관': li_notice,
    '수요기관':  li_demand
})

df.to_csv('나라장터re.csv', encoding="utf-8-sig",index = False)
    

