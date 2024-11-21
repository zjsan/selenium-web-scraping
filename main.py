from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import logging
import time 
import pandas as pd
import numpy as np

service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Login credentials
username = "jpacang@mmsu.edu.ph"
password = "awanpasswordna"

wait = WebDriverWait(driver, 10)

try:
    
    #putting login credentials in the authentication form
    driver.get("https://auth.timeshighereducation.com/auth/realms/THE/protocol/openid-connect/auth?client_id=DataPoints&redirect_uri=https%3A%2F%2Fwww.timeshighereducation.com%2Fdatapoints%2F&state=b7eafe6e-0f6f-4b21-8950-dcda25d30a03&response_mode=fragment&response_type=code&scope=openid&nonce=79c86488-b331-4a3a-848b-bceee80cecab")

    el = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    el.send_keys(username)  # Enter username

    el = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    el.send_keys(password)  # Enter password

    el = wait.until(EC.element_to_be_clickable((By.ID, "kc-login")))
    el.click()

    print("Waiting for the profile icon or similar element to confirm login...")
    driver.get("https://www.timeshighereducation.com/datapoints/")
    print(driver.title)#check for successful login
    print("Login successful!")
    
    #navigating through the page and finding an element
    element = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.XPATH, "//p[@class='chakra-text css-1qawl6f']"))
      )
    print("\n\n",element.text)
    
     #-----Navigating the UI to redirect to the desired page: https://www.timeshighereducation.com/datapoints/sdg/details/1-------
    
    #clicking the sdg impact button
    try:
      click_side_bar = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "//button[@class='chakra-button css-1udhqck']"))
      )
      click_side_bar.click()
      print("side_bar button clicked sucessfully")
      
      #clicking the link to redirect to https://www.timeshighereducation.com/datapoints/sdg/details/1
      click_details_link = driver.find_element(By.XPATH, "//ul[@class='css-1ngfogx']/li[2]/a") #finding this elements
      click_details_link.click()
      print("redirecting to https://www.timeshighereducation.com/datapoints/sdg/details/1")
      
    except TimeoutException:
      logging.error("Sidebar button not clickable.")

    # Wait for the iframe to be present
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='ImpactDetails']")))

    # Switch to the iframe
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='ImpactDetails']"))

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='Header__DownloadSectionWrapper-sc-7l4zmc-1 eSouWg']/p"))#find this element in the web page
    )
    print(element.text)
    print("------page redirect success------")
    
    
except Exception as e:
    logging.error(f"Error in login found: {e}")
    print(driver.page_source)
finally:
    driver.quit()
    
