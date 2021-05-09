import sys
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyperclip #pip3 install pyperclip
import time

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class NcafeWriteAtt:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #self.driver=webdriver.Chrome(chrome_options = chrome_options, executable_path = r'C:/Users/wang/Documents/Python_Pro/webdriver/chrome/chromedriver')
        self.driver=webdriver.Chrome('C:/Users/wang/Documents/Python_Pro/webdriver/chrome/chromedriver')
        self.driver.implicitly_wait(3)

    #네이버 카페 로그인 & 출석 체크 (글 남기기)
    def writeAttendCheck(self):
        self.driver.get('https://nid.naver.com/nidlogin.login')

        pyperclip.copy('내 아이디') #클립보드에 아이디 담기 (ctrl+c)
        self.driver.find_element_by_name('id').click()
        webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy('내 비밀번호') #클립보드에 비밀번호 담기 (ctrl+c)
        self.driver.find_element_by_name('pw').click()
        webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        self.driver.find_element_by_xpath('//*[@id="log.login"]').click()

        time.sleep(5)

        self.driver.implicitly_wait(3)
        #self.driver.get('https://cafe.naver.com/paramsx?iframe_url=/AttendanceView.nhn%3Fsearch.clubid=19756449%26search.menuid=103')
        self.driver.get('https://cafe.naver.com/AttendanceView.nhn?search.clubid=14870242&search.menuid=6')
        self.driver.implicitly_wait(3)

        self.driver.switch_to_frame('cafe_main') #iframe
        self.driver.find_element_by_xpath('//*[@id="cmtinput"]').send_keys('반갑습네다!')
        self.driver.find_element_by_xpath('//*[@id="btn-submit-attendance"]').click()

    #소멸자
    def __del__(self):
        self.driver.quit()
        print("Removed driver Object")

#메인
if __name__=='__main__':
    #객체 생성
    a=NcafeWriteAtt()
    #시작 시간(현재시간 호출)
    start_time=time.time()
    #메서드 실행
    a.writeAttendCheck()
    #종료 시간(현재시간 호출)
    end_time=time.time()
    print("--Total %s seconds--" % (end_time-start_time))
    time.sleep(5)
    #객체 소멸
    del a
