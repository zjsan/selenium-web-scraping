from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='SIvCob']"))
)
try:
    element = driver.find_element(By.XPATH, "//div[@id='SIvCob']")
    print(element.text)
    print("Scrapping success")
    input_element = driver.find_element(By.XPATH, "//textarea[@class='gLFyf']")
    input_element.clear()
    input_element.send_keys("tech with tim" + Keys.ENTER)
except Exception as e:
    print(f"Error: {e}")
    print("error")
finally:
    #time.sleep(10)
    driver.quit