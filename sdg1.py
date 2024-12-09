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

import logging
import time 
import pandas as pd
import numpy as np
import os


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
    
    time.sleep(4)
    #new code- select institution 
    try:
       time.sleep(3)
       element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class = 'chakra-modal__body css-1tcbjr4']"))
        )
       container = WebDriverWait(driver,5).until(
           EC.presence_of_element_located((By.XPATH, "//div[@class = 'css-kfokcf']"))
       )
       mmsu = driver.find_element(By.XPATH, "//div[@class = 'css-18oq3rf']/img[@alt ='Mariano Marcos State University logo']")
       mmsu.click()
    except Exception as e:
        print(f"Error: {e}")
        print("Error in the Select an institution page")
    
    #navigating through the page and finding an element
    element = WebDriverWait(driver, 10).until(
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

    #if successful redirect
    # Wait for the iframe to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='ImpactDetails']")))

    # Switch to the iframe
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@id='ImpactDetails']"))

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='Header__DownloadSectionWrapper-sc-7l4zmc-1 eSouWg']/p"))#find this element in the web page
    )
    print(element.text)
    print("------page redirect success------")
    
    #interacting with the selecting region and country section of the page
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class = 'PeerSelectWrapper__Wrapper-sc-brqol7-1 kACRoa']"))
    )
    
    #entering input in the country/region selection
    try:
        country_name = "Philippines"
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class = 'LocationSearch__Container-sc-1dp07t6-0 dhVVKS']"))
        )
        print("found element in the country selection")
        country_input = driver.find_element(By.XPATH, "//input[@id='downshift-2-input']")
        driver.find_element(By.XPATH, "//div[@role='combobox']").__setattr__("aria-expanded","true")#set combo box value to true to see list of regions/countriess
        print("----typing country name-----")
        
        #individually type the country name in the input field
        #hope it will work this time kase pagod na ako putanginaaaaaaaaaaa
        for char in country_name:
            country_input.send_keys(char)   
            time.sleep(0.3)

            if char == "s":
                country_input.send_keys(Keys.ARROW_DOWN)
                country_input.send_keys(Keys.ENTER)
        print("-----Sucessfully selected region/country------")
          
    except Exception as e:
        print(f"Error: {e}")
        print("Can't select country")

    # Selecting elements from universities
    try:
        # Selecting the container for the list of universities
        element = driver.find_element(By.XPATH, "//div[@class='PeerSelect__Container-sc-cfs1fm-0 kNqusN']")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='PeerSelect__InstitutionName-sc-cfs1fm-6 jBTLtN']"))
        )
        print("\nFound universities\n")

        # Select all university buttons
        university_name_buttons = driver.find_elements(By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']/li/button")
        university_length = len(university_name_buttons)
        print(f"Total universities found: {university_length}")

        batch_size = 35  # Number of universities to process per batch
        click_count = 0  # Counter for clicks

        # Process universities in batches
        for batch_start in range(0, university_length, batch_size):
            # Reset selections if not the first batch
            if batch_start > 0:
                try:
                    reset_button = driver.find_element(By.XPATH, "//button[text()='Reset benchmark']")
                    reset_button.click()
                    time.sleep(2)  # Allow time for reset
                    print("Selections reset for the next batch")
                except Exception as e:
                    print("No reset button found or reset failed")

            # Select universities in the current batch
            for index in range(batch_start, min(batch_start + batch_size, university_length)):
                try:
                    university_name_buttons[index].click()
                    click_count += 1
                    print(f"Selected: {university_name_buttons[index].text}")
                    time.sleep(0.3)  # Pause for UI responsiveness
                except Exception as e:
                    print(f"Error clicking university button at index {index}: {e}")

            print(f"Batch {batch_start // batch_size + 1} - Selected {click_count} universities")

            # Apply selections
            try:
                print("\n---Clicking Apply button---\n")
                apply_button = driver.find_element(By.XPATH, "//button[@class='PeerSelect__ApplyButton-sc-cfs1fm-9 frSOwt']")
                apply_button.click()
                time.sleep(2)

                # Click the Table button
                print("---Clicking Table button---\n")
                table_button = driver.find_element(By.XPATH, "//button[@class='TabSelector__Tab-sc-x9oxnj-1 ennyZL']")
                table_button.click()
                time.sleep(2)
                print("---Table button clicked---")

                # Download the Excel file for the current batch
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='DownloadButton__TriggerButton-sc-plxomw-1 bTWVdx']"))
                )
                download_button = driver.find_element(By.XPATH, "//button[@class='DownloadButton__TriggerButton-sc-plxomw-1 bTWVdx']")
                download_button.click()
                print("\n---Download button clicked---\n")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='DownloadButton__Download-sc-plxomw-4 hDjlSG']"))
                )
                download_excel = driver.find_element(By.XPATH, "//button[@class='DownloadButton__Download-sc-plxomw-4 hDjlSG']")
                download_excel.click()
                print(f"\n---Batch {batch_start // batch_size + 1} downloaded---\n")
                time.sleep(5)  # Wait for download completion

            except Exception as e:
                print(f"Error during Apply/Table/Download steps in Batch {batch_start // batch_size + 1}: {e}")

        print("\nAll batches processed successfully\n")

    except Exception as e:
        print(f"Error: {e}")
        print("Error fetching universities")

    # Final processing or merging (if needed)
    print("\n-----Scraping Done-----")

except Exception as e:
    logging.error(f"Error in login found: {e}")
    print(driver.page_source)
finally:
    time.sleep(10)
    driver.quit()
    
