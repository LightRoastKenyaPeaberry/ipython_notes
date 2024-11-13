'''
显式等待
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium import webdriver 

driver= webdriver.Chrome() 

# 1. 创建一个等待对象 
wait = WebDriverWait(driver, 30, 0.2)

# 2. 定义元素查找对象 
# located = ('locate_way', 'locate_expr')
located = (By.XPATH, '//input[@id="u"]')

# 3. 定位的等待条件 
conditions = EC.visibility_of_element_located(located)
# or 等待元素可点击
# conditions = EC.element_to_be_clickable(located)

# 4. 通过等待计时器对象去找
wait.until(conditions)


# 一句话表示 
WebDriverWait(driver, 30, 0.2).until(
    EC.visibility_of_element_located((By.XPATH, '//input[@id="u"]'))
)
