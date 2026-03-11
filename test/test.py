from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time 
import os

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

remote_url = os.getenv("SELENIUM_URL",  "http://selenium:4444")

driver = None
for i in range(10):  # Try 10 times
    try:
        print(f"Attempting to connect to Selenium (Attempt {i+1}/10)...")
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        print("Connected successfully!")
        break
    except WebDriverException:
        print("Selenium not ready yet, sleeping 5s...")
        time.sleep(5)

if not driver:
    print("Could not connect to Selenium after multiple attempts.")
    exit(1) 

try:
    driver.get("https://www.google.com")#url to scrape

    wait = WebDriverWait(driver, 10)

    element = wait.until(
        EC.presence_of_element_located((By.ID, "SIvCob"))
    )
    
    print(element.text)
    print("Scrapping success")
    input_element = driver.find_element(By.XPATH, "//textarea[@class='gLFyf']")
    input_element.clear()
    input_element.send_keys("tech with tim" + Keys.ENTER)
    print("Search successful")
except Exception as e:
    print(f"Error: {e}")
    print("error")
finally:
    #time.sleep(10)
    driver.quit