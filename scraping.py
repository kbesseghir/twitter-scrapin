import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to add a newline character at the beginning of each tweet text
def add_newline_to_text(df):
    df['text'] = df['text'].apply(lambda x: '\n' + x)
    return df

# Webdriver setup
web = "https://twitter.com/i/flow/login"
driver = webdriver.Chrome()
driver.get(web)
driver.maximize_window()

# Wait for login box to appear
login_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@class="css-1dbjc4n r-ywje51 r-nllxps r-jxj0sb r-16wqof r-1dye5f7"]'))
)

# Enter username and click next
username = login_box.find_element(By.TAG_NAME, 'input')
username.send_keys("write your username")
next_button = login_box.find_element(By.XPATH, "//div[@class='css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu']")
next_button.click()

# Wait for password input field to appear and enter password
time.sleep(20)  # Adjust sleep time if necessary
password = driver.find_element(By.XPATH, "//input[@name='password']")
password.send_keys("write your password")

# Click the login button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]'))
)
login_button.click()

# Navigate to the explore page
time.sleep(15)  # Adjust sleep time if necessary
main_page = driver.find_element(By.XPATH, '//div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]')
time.sleep(15)  # Adjust sleep time if necessary
explore = main_page.find_element(By.XPATH, '//a[@href="/explore"]')
explore.click()
time.sleep(20)  # Adjust sleep time if necessary

# Search for tweets
search_label = driver.find_element(By.XPATH, '//input[@role="combobox"]')
search_word = input('Please enter the search term: ')
search_label.send_keys(search_word)
search_label.send_keys(Keys.RETURN)

# Scroll and retrieve tweets
time.sleep(13)  # Adjust sleep time if necessary
section = main_page.find_element(By.XPATH, '//section[@role="region"]')
user_data = []
text_data = []
scrolling = True
tweet_ids = set()

while scrolling:
    tweets = section.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

    for tweet in tweets[:15]:
        text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        name = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
        tweet_list = [name, text]
        tweet_id = ''.join(tweet_list)

        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(name)
            text_data.append(text)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            scrolling = False
            break
        else:
            last_height = new_height
            break

# Close the web driver
driver.quit()

# Storing the data into a DataFrame
df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})

# Add newline character to tweet text
df_tweets = add_newline_to_text(df_tweets.copy())

# Export the data to a CSV file
df_tweets.to_csv('tweetsScrolling.csv', index=False)
