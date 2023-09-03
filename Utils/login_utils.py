from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

from Utils import login_option as LO
import pyautogui
import time

# 로그인할 사이트 목록 딕셔너리 정의

class LoginBot:
    def __init__(self, site):
        # 엣지 웹 드라이버
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Edge(options= options)
        
        # 브라우저 해상도 설정
        self.driver.set_window_size(1600, 900)
        # 로그인하려는 사이트로 이동
        try:
            self.driver.get(site)
            # 10초 이하 대기
            self.driver.implicitly_wait(time_to_wait=10)
        except:
            print("Error occured")

    # 크롤러 종료
    def kill(self):
        self.driver.quit()

    # 로그인을 수행하는 메서드입니다.
    def login(self, id, ps):
        login_box = self.driver.find_element(By.XPATH, '//*[@id="login_id"]')
        login_box.send_keys(id)
        login_box = self.driver.find_element(By.XPATH, '//*[@id="login_pw"]')
        login_box.send_keys(ps)        
        login_box.send_keys(Keys.ENTER)
        learning_box = self.driver.find_element(By.XPATH, '//*[@id="mainNav"]/li[2]/a')

    def self_learning(self, place : str, age:int):
        XPATH_Range = ['tr[1]/td[4]/span/input', 'tr[2]/td[4]/span/input', 'tr[3]/td[4]/span/input']
        self.driver.implicitly_wait(time_to_wait=10)
        learning_box = self.driver.find_element(By.XPATH, '//*[@id="mainNav"]/li[2]/a')
        learning_box.send_keys(Keys.ENTER)
        learning_box = self.driver.find_element(By.XPATH, '//*[@id="mainNav"]/li[2]/ul/li[2]/a')
        learning_box.send_keys(Keys.ENTER)  
        for i in XPATH_Range:
            time.sleep(4)
            learning_box = self.driver.find_element(By.XPATH, '//*[@id="stu_subpg1_1"]/form/div[3]/div/div[2]/div/div/table/tbody/' + i)
            learning_box.send_keys(Keys.ENTER)
            time.sleep(4)
            learning_box = self.driver.find_element(By.XPATH, '//*[@id="cls_idx' + str(LO.option.index(place) - age) +  '"]')
            self.driver.execute_script("arguments[0].click();", learning_box)
            time.sleep(2)
            learning_box = self.driver.find_element(By.XPATH, '//*[@id="subpg1_3form"]/div/div/button[1]')
            learning_box.send_keys(Keys.ENTER)


    # 스크린샷 메서드
    def save_screenshot(self):
        self.driver.save_screenshot("test.png")
