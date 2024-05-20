from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager

def crawling_all(url):

    # 속도 향상을 위한 여러 세팅들
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    # options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    session = requests.Session()
    headers = {
        "User-Agent": "user value"}

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    # Session 객체에 HTTPAdapter 장착
    # 요청 처리할 때 사용되는 설정 커스터마이즈
    session.mount('http://', HTTPAdapter(max_retries=retries))


    driver = webdriver.Chrome(options=options)

    # 웹페이지 열기
    res = driver.get(url)

    # 암묵적 대기 설정
    driver.implicitly_wait(30)

    list_sheet = []
    num = 0
    actions = ActionChains(driver)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button/span[2]'))).click()
                    # 공고이름
        posting_name = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/h1').text
                    # 기업이름    
        cop_name = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/a').text
                    # 공고링크  
        position = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/p/span').text
                    # 주요업무
        major_task = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[1]/p/span').text
                    # 자격요건
        qualification =  driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[2]/p/span').text
                    # 우대사항
        preferential = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[3]/p/span').text
                    # 해택 및 복지
        benefits = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[4]/p/span').text
                    # 기업 링크
                    
                    # 수집된 정보 리스트 추가
        list_sheet.append([posting_name, cop_name, position, major_task, qualification, preferential, benefits])
    except Exception as e:
        print('Error occurred:', str(e))
        print('finish')
    return list_sheet