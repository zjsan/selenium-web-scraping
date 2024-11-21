from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.
import time 

service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

time.sleep(10)

driver.quit