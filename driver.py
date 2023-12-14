import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from config import instagram_username, instagram_password

login_page = 'https://www.instagram.com/'

login_box_xpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
password_box_xpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
login_button_xpath = '//*[@id="loginForm"]/div/div[3]'
search_button_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div'
search_box_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input'
users_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a'
subscribe_button_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button'
notify_button_xpath = '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
profile_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a/div'


def save_cookies_to_file(cookies):
    with open('cookies.txt', 'w') as file:
        file.write(json.dumps(cookies))


def get_cookies_from_file():
    with open('cookies.txt', 'r') as file:
        data = file.read()
        if not data:
            return None
        cookies = json.loads(data)
    return cookies


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
    # options.add_argument('--headless')
    options.add_argument("--window-size=3840,2160")
    driver_path = Service(r"C:\Python\ChromeDriver\chromedriver.exe")

    driver = webdriver.Chrome(service=driver_path, options=options)
    cookies = get_cookies_from_file()
    if not cookies:
        driver.get(login_page)
        time.sleep(5)
        login_box = driver.find_element(By.XPATH, login_box_xpath)
        login_box.clear()
        login_box.send_keys(instagram_username)
        time.sleep(5)
        password_box = driver.find_element(By.XPATH, password_box_xpath)
        password_box.clear()
        password_box.send_keys(instagram_password)
        time.sleep(2)
        driver.find_element(By.XPATH, login_button_xpath).click()
        time.sleep(20)
        cookies = driver.get_cookies()
        save_cookies_to_file(cookies)

    else:
        driver.get(login_page)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(login_page)
    time.sleep(3)
    notify = driver.find_element(By.XPATH, notify_button_xpath)
    if notify:
        notify.click()
    time.sleep(5)
    driver.find_element(By.XPATH, profile_xpath).click()
    return driver


driver = get_driver()


def subscribe(name: str):
    driver.find_element(By.XPATH, search_button_xpath).click()
    driver.find_element(By.XPATH, search_box_xpath).send_keys(name)
    time.sleep(5)
    links = driver.find_elements(By.XPATH, users_xpath)
    for link in links:
        if link.text.split('\n')[0] != name:
            continue
        else:
            link.click()
            time.sleep(5)
            driver.find_element(By.XPATH, subscribe_button_xpath).click()
            time.sleep(3)
            driver.find_element(By.XPATH, profile_xpath).click()
            return True
    driver.find_element(By.XPATH, search_button_xpath).click()
    return False
