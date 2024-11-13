from selenium import webdriver
from selenium.webdriver.common.by import By
import time 



# 1. selenium打开浏览器
driver = webdriver.Chrome() 

# 2. 打开要操作的页面
url = 'https://liuyan.people.com.cn/threads/list?checkStatus=0&fid=1427&formName=%E9%93%B6%E5%B7%9D%E5%B8%82%E5%A7%94%E4%B9%A6%E8%AE%B0%E8%B5%B5%E6%97%AD%E8%BE%89&position=0&province=44&city=479&saveLocation=44&pForumNames=%E5%AE%81%E5%A4%8F%E5%9B%9E%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA&pForumNames=%E9%93%B6%E5%B7%9D%E5%B8%82'
driver.get(url)

driver.implicitly_wait(7)

time.sleep(3)

# 定位到"查看更多"
elem = driver.find_element(by=By.XPATH, value='//*[@class="mordList"]')
elem.location_once_scrolled_into_view

time.sleep(10)

driver.quit() 