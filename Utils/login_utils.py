from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyautogui

# 로그인할 사이트 목록 딕셔너리 정의

class LoginBot:
    def __init__(self, site):
        # 엣지 웹 드라이버
        self.driver = webdriver.Edge(executable_path="msedgedriver.exe")
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
        pyautogui.press("tab")
        # 아이디 입력
        pyautogui.write(id)
        # tab 키
        pyautogui.press("tab")
        # 비밀번호 입력
        pyautogui.write(ps)
        # 엔터키 입력
        pyautogui.press("enter")
        # 5초 대기
        self.driver.implicitly_wait(time_to_wait=10)

    def self_learning(self):
        learning_box = self.driver.find_element(By.XPATH, '//*[@id="mainNav"]/li[2]/a')
        learning_box.send_keys(Keys.ENTER)
        learning_box = self.driver.find_element(By.XPATH, '//*[@id="mainNav"]/li[2]/ul/li[2]/a')
        learning_box.send_keys(Keys.ENTER)

    # 스크린샷 메서드
    def save_screenshot(self):
        self.driver.save_screenshot("test.png")
