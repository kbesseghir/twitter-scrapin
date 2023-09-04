from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

web = "https://twitter.com/"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

# wait of 6 seconds to let the page load the content
time.sleep(6)  

login =driver.find_element(By.XPATH,'//a[@href="/login"]')
login.click()

login_box=driver.find_element(By.XPATH,'//div[@class="css-1dbjc4n r-ywje51 r-nllxps r-jxj0sb r-16wqof r-1dye5f7"]')
username = login_box.find_element(By.TAG_NAME,'input')