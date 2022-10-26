import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from decouple import config

# -------------------- CONSTANTS -------------------- #
# - Twitter Config
TWITTER_EMAIL = config("TWITTER_EMAIL")
TWITTER_PASSWORD = config("TWITTER_PASSWORD")
TWITTER_NUMBER = config("TWITTER_NUMBER")
# - internet
PROMISED_DOWN = 100
PROMISED_UP = 10
PROVIDER = "Megacable"
# - URLs
SPEED_TEST = "https://www.speedtest.net/en"
TWITTER = "https://twitter.com/?lang=es"


# -------------------- FUNCTIONS -------------------- #
def tweet(up, down):
    driver.get(TWITTER)

    # - Sign in button
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a').click()

    # - Sending credentials
    time.sleep(2)
    email_input = driver.find_element(By.XPATH,
                                      '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]'
                                      '/div/div/div/div[5]/label/div/div[2]/div/input')
    email_input.send_keys(TWITTER_EMAIL)
    driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div'
                                  '/div/div/div[6]').click()
    time.sleep(2)

    try:
        tel_number = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div'
                                                   '/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        tel_number.send_keys(TWITTER_NUMBER)
    except NoSuchElementException:
        pass
    else:
        driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]'
                                      '/div[2]/div[2]/div/div/div/div/div').click()

    time.sleep(2)

    password_input = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div'
                                                   '/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]'
                                                   '/input')
    password_input.send_keys(TWITTER_PASSWORD)

    # - Sign in final button
    driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]'
                                  '/div[2]/div/div[1]/div/div/div').click()

    time.sleep(2)

    # - Message
    message = f"Hey {PROVIDER}, why is my internet speed {down}down/{up}up " \
              f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"

    # - Write a message
    message_input = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div'
                                                  '/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]'
                                                  '/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div'
                                                  '/div/div/div/div[2]/div/div/div/div')
    message_input.send_keys(message)

    # - Tweet button
    driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]'
                                  '/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]').click()


# -------------------- SCRIPT -------------------- #
# - Selenium Config
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(SPEED_TEST)
driver.maximize_window()

# - Go button
driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a').click()

time.sleep(45)

# - Close Ad
driver.find_element(By.XPATH,
                    '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/a').click()

# - Getting internet speed
speed_down = float(driver.find_element(By.XPATH,
                                       '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]'
                                       '/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
speed_up = float(driver.find_element(By.XPATH,
                                     '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]'
                                     '/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)

# - Comparing speeds
if PROMISED_DOWN > speed_down or PROMISED_DOWN > speed_up:
    tweet(speed_up, speed_down)

time.sleep(60)

driver.quit()


