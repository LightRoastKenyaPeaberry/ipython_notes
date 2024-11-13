from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium import webdriver 
import time 

driver= webdriver.Chrome() 
driver.get('http://www.qqmail.com')

driver.implicitly_wait(5)

# 切换到相应的iframe网页中
driver.switch_to.frame(1)
driver.switch_to.frame('ptlogin_iframe')

login_qq = driver.find_element(by=By.XPATH, value='//a[@id="switcher_plogin"]')

login_qq.click() 


user = driver.find_element(by=By.XPATH, value='//input[@id="u"]')
user.send_keys('635663494')

pwd = driver.find_element(by=By.XPATH, value='//input[@id="p"]')
user.send_keys('5689230Sophie.')

driver.find_element(by=By.XPATH, value='//input[@id="login_button"]').click() 
time.sleep(5)

driver.quit() 
