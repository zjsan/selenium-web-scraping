#copy of scrap.py 
#intended for testing

from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException

import logging
import time 
import pandas as pd
import numpy as np
import os       
import pyautogui

# Desired upload directory - google drive
download_directory = r"C:\Users\User\Documents\SDG Datas\Scraping\Scrap data"

# Desired upload directory - windows os
folder_path = r"C:\Users\User\Documents\SDG Datas\Scraping\Scrap data"

# Verify directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# Remove incognito mode (it might override preferences)
# chrome_options.add_argument("--incognito")  
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Helps bypass detection

# Set up preferences for downloads
prefs = {
    "download.default_directory": download_directory,  # Set custom download directory
    "download.prompt_for_download": False,            # Disable download prompt
    "directory_upgrade": True,                        # Allow directory change
    "safebrowsing.enabled": True,                     # Enable safe browsing
    "profile.default_content_settings.popups": 0      # Disable popups
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
service = Service(executable_path="chromedriver.exe")  # Update path as needed
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
  
  folder_path = r"C:\Users\User\Documents\SDG Datas\Scraping\Scrap data"
  # Navigate to Google Drive
  driver.get("https://drive.google.com/drive/folders/1qFRxwU4IqJUXweyU_ShgL_YHnTxcIri0")

  #finding and clicking sign in button 
  sign_in = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, "//a[@class='gb_Ta gb_yd gb_pd gb_gd']"))
  )
  sign_in.click()
  
  # Login credentials
  try:
    time.sleep(2)
    print("Attempting to login Google Drive authentication")
    #must hid credentials
    username = "zdsantos@mmsu.edu.ph"
    password = "Cur63706"
    wait = WebDriverWait(driver, 10)
    el = wait.until(EC.element_to_be_clickable((By.ID, "identifierId")))
    el.send_keys(username)  # Enter username
    
    time.sleep(1)
    email_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']"))
    )
    email_button.click()
    
    el = wait.until(EC.element_to_be_clickable((By.NAME, "Passwd")))
    el.send_keys(password)  # Enter password
    password_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b']"))
    )
    password_button.click()
    print("Succesful authentication\n")
  except Exception as e:
      print(f"Error: {e}")
      print("Error in the login process")
  
  #brbsPe Ss7qXc a-qb-d
  #clicking the new button
  try:
    
    time.sleep(1)
    print("Attempting to click new button")
    new_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='brbsPe Ss7qXc a-qb-d']"))
    )
    new_button.click()
    print("New button clicked successfully\n")

    try:
        # Click on "Folder upload"
        folder_upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Folder upload']"))
        )
        folder_upload_button.click()  
        
        # Enter the folder path in the file dialog 
        pyautogui.write(folder_path, interval=0.25)
        
        time.sleep(1)
        pyautogui.press('enter')#select folder
        pyautogui.press('enter')#upload
        
        # Wait for the upload dialog and accept it 
        # time.sleep(2) 
        # # Adjust this based on the alert appearance time
        # try: 
        #   alert = driver.switch_to.alert alert.accept() 
        # except NoAlertPresentException:
        # print("No alert present)"
    except:
        print(f"Error: {e}")
        print("Error in folder upload")
  except Exception as e:
      print(f"Error: {e}")
      print("Error in clicking button")
  
#   # Wait for the "New" button to be clickable
#   new_button = WebDriverWait(driver, 10).until(
#       EC.element_to_be_clickable((By.XPATH, "//span[text()='New']"))
#   )
#   new_button.click()

#   # Click on "Folder upload"
#   folder_upload_button = WebDriverWait(driver, 10).until(
#       EC.element_to_be_clickable((By.XPATH, "//div[text()='Folder upload']"))
#   )
#   folder_upload_button.click()

#   # Select the folder to upload
#   file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
#   file_input.send_keys(folder_path)

  # Wait for the upload to complete (you might need to adjust this based on the file size)
  time.sleep(60)  # Adjust this value as needed
except Exception as e:
    print(f"Error: {e}")
    print("Error in the google drive folder")
finally:
    time.sleep(10)
    driver.quit()
    
