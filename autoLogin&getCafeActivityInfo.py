﻿import sys
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyperclip #pip3 install pyperclip
import time
from bs4 import BeautifulSoup
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class NcafeGetActiv:

    def __init__(self):
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #self.driver=webdriver.Chrome(chrome_options = chrome_options, executable_path = r'C:/Users/wang/Documents/Python_Pro/webdriver/chrome/chromedriver')
        self.driver=webdriver.Chrome('C:/Users/wang/Documents/Python_Pro/webdriver/chrome/chromedriver')
        self.driver.implicitly_wait(3)

    #네이버 카페 로그인 & 카페 활동내역 수집
    def getHistoryInfo(self):
        self.driver.get('https://nid.naver.com/nidlogin.login')

        pyperclip.copy('아이디') #클립보드에 아이디 담기 (ctrl+c)
        self.driver.find_element_by_name('id').click()
        webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy('비밀번호') #클립보드에 비밀번호 담기 (ctrl+c)
        self.driver.find_element_by_name('pw').click()
        webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        self.driver.find_element_by_xpath('//*[@id="log.login"]').click()
        time.sleep(5)

        #활동내역페이지 접속 및 페이지추출
        self.driver.implicitly_wait(5)
        self.driver.get('https://cafe.naver.com/CafeHistoryView.nhn?clubid=14870242')
        self.driver.implicitly_wait(5)
        self.driver.switch_to_frame('cafe_main') #iframe
        #print(self.driver.page_source)
        self.driver.implicitly_wait(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        #print(soup)
        #main-area > div > table

        #DF용 리스트 생성
        dateList=[]
        historyDetailsList=[]

        #출력 및 리스트 추가
        li=soup.select('#main-area > div > table')
        #print(li)
        for i in li:
            year=i.select_one('tbody > tr:nth-child(1) > td.td_year').string.strip()
            li2=i.select('tbody > tr')
            #print(li2)
            for j in li2:
                if j.select_one('td.td_date') is not None and j.select_one('td.td_desc') is not None:
                    monthDay=j.select_one('td.td_date').string.strip()
                    historyDetails=j.select_one('td.td_desc').text.strip()
                    date=year+"."+monthDay[:-1]

                    #출력
                    print(date)
                    print(historyDetails)

                    #리스트에 추가
                    dateList.append(date)
                    historyDetailsList.append(historyDetails)

        #데이터프레임 작성
        data = { 'date' : dateList, 'historyDetails': historyDetailsList}
        df = pd.DataFrame(data)
        print(df)
        return df

        timp.sleep(3)

    #csv로 저장
    def saveCsv(self, df):
        df.to_csv('C:/Users/wang/Documents/Python_Pro/webdriver/chrome/history.csv',index=False)


    #소멸자
    def __del__(self):
        self.driver.quit()
        print("Removed driver Object")

#메인
if __name__=='__main__':
    #객체 생성
    a=NcafeGetActiv()
    #시작 시간(현재시간 호출)
    start_time=time.time()
    #메서드 실행
    a.saveCsv(a.getHistoryInfo())
    #종료 시간(현재시간 호출)
    end_time=time.time()
    print("--Total %s seconds--" % (end_time-start_time))
    time.sleep(5)
    #객체 소멸
    del a
