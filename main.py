from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

try:
    element = driver.find_element(By.XPATH, "//div[@id='SIvCob']")
    print(element.text)
    print("Scrapping success")
except Exception as e:
    print(f"Error: {e}")
    print("error")
finally:
    time.sleep(10)
    driver.quit