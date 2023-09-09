from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


web = "https://twitter.com/i/flow/login"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

# wait of 6 seconds to let the page load the content

# login =driver.find_element(By.XPATH,'//a[@href="/login"]')
# login.click()
# print('successfully logged in')

login_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="css-1dbjc4n r-ywje51 r-nllxps r-jxj0sb r-16wqof r-1dye5f7"]'))
        )

username = login_box.find_element(By.TAG_NAME,'input')
username.send_keys("write ur username ")
next_button=login_box.find_element(By.XPATH,"//div[@class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu']")
next_button.click()
print('successfully logged in')
time.sleep(20)
password = driver.find_element(By.XPATH, "//input[@name='password']")   
print('successfully logged in')

password.send_keys("write ur passw")
print('successfully logged in')
login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]'))
        )
login_button.click()
print('successfully logged in')


# driver.get('https://twitter.com/home')

# driver.switch_to.window(driver.window_handles[-1])
time.sleep(15)
main_page = driver.find_element(By.XPATH,'//div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]')
print('successfully logged in')
time.sleep(5)
explore=main_page.find_element(By.XPATH,'//a[@href="/explore"]')
explore.click()
print('search successfully')

print(main_page)
time.sleep(20)

search_label=driver.find_element(By.XPATH,'//input[@role="combobox"]')
print('search successfully')

search_word=input('please enter the word u want to search: ')
search_label.send_keys(search_word)
search_label.send_keys(Keys.RETURN)
print('search successfully')

# search_button=driver.find_element(By.XPATH,'//div[@class="css-1dbjc4n r-7q8q6z r-6koalj r-1777fci"]')
# search_button.click()
time.sleep(13)
section =main_page.find_element(By.XPATH,'//section[@role="region"]')
tweets=section.find_elements(By.XPATH,'//article[@data-testid="tweet"]')
print('found succ')
user_data = []
text_data = []
for tweet in tweets:
    text=tweet.find_element(By.XPATH,'.//div[@data-testid="tweetText"]').text
    print('good')
    name =tweet.find_element(By.XPATH,'.//span[contains(text(), "@")]').text

    user_data.append(name)  # appending the first element of tweet_list (user)
    text_data.append(text)
    print('secc')


driver.quit()
# Storing the data into a DataFrame and exporting to a csv file
df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets.csv', index=False)
print(df_tweets)