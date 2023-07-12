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


list_org = []
list_title = []
list_career = []
list_education = []
list_recruit = []
list_location = []
list_work = []


keyword = '공간정보'
for i in range(1, 21):
    url = f'https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={i}'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    infos = soup.select('li.list-post')
    infos = infos[:20]

    for info in infos:
        org = info.select_one('.name.dev_view').text
        title = info.select_one('.title.dev_view').text
        career = info.select_one('p.option>span:nth-of-type(1)').text
        education = info.select_one('p.option>span:nth-of-type(2)').text
        recruit = info.select_one('p.option>span:nth-of-type(3)').text
        location = info.select_one('p.option>span:nth-of-type(4)').text
        work = info.select_one('p.etc').text

        list_org.append(org)
        list_title.append(title)
        list_career.append(career)
        list_education.append(education)
        list_recruit.append(recruit)
        list_location.append(location)
        list_work.append(work)

df = pd.DataFrame({
    '채용기관': list_org,
    '공고명': list_title,
    '커리어제한': list_career,
    '학력' : list_education,
    '타입': list_recruit,
    '지역': list_location,
    '담당업무': list_work
})

df.to_csv('잡코리아.csv', encoding='utf-8-sig', index = False)
df.head()
    
    
