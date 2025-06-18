"""
Python Script for automating data collection in the Times Higher Education - Datapoints Website

- ASEAN Countries => Brunei Darussalam, Cambodia, Indonesia, Malaysia, Philippines, Thailand, Viet Nam 
 ( Available Countries in the Datapoints)

Note: 
 - Ensure that the chromedriver.exe has the same version as the current version of the chrome web browser
 - Adjust time delays in the time.sleep(n) function if needed
 - Specify the name of target default country for data collection
 - Default Reference group for scraping is "World-Wide" 
 
"""



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

import logging
import time 
import pandas as pd
import numpy as np
import os


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Helps bypass detection

# Define the custom download directory (ensure it exists)
download_dir = r"C:\Users\User\Documents\SDG Datas\Scraping\Scrap data"  # Use raw string for Windows paths

# Ensure the directory exists
os.makedirs(download_dir, exist_ok=True)

chrome_options.add_experimental_option('prefs', {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})


service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service=service)


# Login credentials
username = "jpacang@mmsu.edu.ph"
password = "awanpasswordna"

#Reference group selection
refenceGroup = "" #manually enter the desired refence group

country_name = "Vietnam" #change to specific country selection

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
    try:
        element = WebDriverWait(driver, 13).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='chakra-text css-1qawl6f']"))
        )
        print("\n\n",element.text)
    except TimeoutException:
        print("Error in the landing page after login.")   
         
    try:
      time.sleep(1)
      click_side_bar = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "//button[@class='chakra-button css-1udhqck']"))
      )
      click_side_bar.click()
      print("side_bar button clicked sucessfully")
      
      time.sleep(3)
      #clicking the link to redirect to https://www.timeshighereducation.com/datapoints/sdg/details/1
      click_details_link = driver.find_element(By.XPATH, "//ul[@class='css-1ngfogx']/li[2]/a") #finding this elements
      click_details_link.click()
      print("redirecting to https://www.timeshighereducation.com/datapoints/sdg/details/1")
      
    except TimeoutException:
      logging.error("Sidebar button not clickable.")

    #if successful redirect
    time.sleep(1)
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
    
    time.sleep(1)
    try:
        
        links_click = 0#clicked counter
        links_length = 17 #number for the remaining sdg link redirection

        #main loop for page navigation
        for i in range(links_length):
            
            time.sleep(3)  
            driver.switch_to.default_content() #leave frame
            # Wait for the iframe to load - new page
            
            #insert logic for page refresh?
            #for unexpected page refresh
            max_retries = 3
            attempt = 0
            while attempt < max_retries:
                try:
                    time.sleep(3)
                    print("Finding web page's iframe")
                    element = WebDriverWait(driver, 10).until
                    (EC.presence_of_element_located((By.XPATH, "//iframe[@id='ImpactDetails']")))
                    print("---Iframe found---")
                    time.sleep(1)
                    print("\nProceeding to switch from default view to iframe\n")
                    break
                except TimeoutException:
                    attempt += 1
                    print("Iframe not found. Check if redirection worked.")
                    print(f"Attempting to find Iframe. Retrying... ({attempt}/{max_retries})")
                except Exception as e:
                    raise RuntimeError("Failed to locate Iframe") from e       
            #Switch to the iframe
            try:
                time.sleep(2)
                iframe = driver.find_element(By.XPATH, "//iframe[@id='ImpactDetails']")
                driver.switch_to.frame(iframe)
                print("\nSwitched to iframe")
                time.sleep(1)
            except TimeoutException:
                print("Iframe not found on this page. Skipping...")
                break
                    
            #Wait for and print the desired element -- to check if page load is sucessfull
            try:
                element = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class='SDGTitle__TitleWrapper-sc-4tg6e9-0 kfKJKx']"))
                )
                page_title = driver.find_element(By.XPATH, "//h1[@class='SDGTitle__TitleWrapper-sc-4tg6e9-0 kfKJKx']")
                print(page_title.text)
                
                element = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='Header__DownloadSectionWrapper-sc-7l4zmc-1 eSouWg']/p"))
                )
                print(element.text)
                page_title = driver.find_element(By.XPATH, "//h1[@class='SDGTitle__TitleWrapper-sc-4tg6e9-0 kfKJKx']") 
                print(page_title.text)
                print("\n------Page redirect success------\n")
                
            except TimeoutException:
                print("Desired element not found on this page.")
                print("Exiting the program loop")
                break
            
            #----Scraping Logic here-----
            try: 
                
                if refenceGroup == "":
                    print("Default Worldwide reference group is selected")
                else:
                    
                    #finding and selecting the reference group input field
                    element = WebDriverWait(driver,5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='LocationSearch__Container-sc-1dp07t6-0 dhVVKS']//input"))
                    )
                    reference_group_input = driver.find_element(By.XPATH, "//div[@class='LocationSearch__Container-sc-1dp07t6-0 dhVVKS']//input")
                    print("Selected {} as the reference group".format( refenceGroup))
                    #typing the reference group in the input field
                    reference_group_input.clear()
                    reference_group_input.click()#to prevent unwanted country name 
                    for char in refenceGroup:
                        
                        reference_group_input.send_keys(char)
                        time.sleep(0.4)

                    # After typing, select from dropdown
                    reference_group_input.send_keys(Keys.ARROW_DOWN)
                    reference_group_input.send_keys(Keys.ENTER) 
                    
            except Exception as e:
                    print("Can't find the reference group input value")
                    print(f"Error: {e}")   
                    
                    
            filter_by_top_20 = False #keeping it at false to select the default filtering of SDG Peformance, otherwise it will filter the top 20 institutions   
            
            if filter_by_top_20:
                try:
                    
                    print("Finding filter input")
                    element = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='the02318 the02319']"))
                    )
                    print("Filter input located")
                    filter_input = driver.find_element(By.XPATH, "//ul[@class='the02318 the02319']")
                    filter_input.click()   
                    top20 = driver.find_element(By.XPATH, "//ul[@class='the02318 the02319']/li[2]")    
                    print("Selected {} filter as ".format(top20))
                    top20.click()
                    print("Successfully selected filter")
                    
                except Exception as e:
                    print("Can't find the filter selection value")
                    print(f"Error: {e}")   
                        
                
            #Step 1: entering input in the country/region selection
            try:
                #Scraping Logic
                time.sleep(2)
                print("Finding location container")
                element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class = 'LocationSearch__Container-sc-1dp07t6-0 dhVVKS']"))
                )
                print("Found location container")
                country_input = driver.find_element(By.XPATH, "//input[@id='downshift-2-input']")
                  
                #Checking Region/Country container if the desired country is present    
                try:
                    time.sleep(1)
                    element = WebDriverWait(driver,7).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='LocationSearch__Container-sc-1dp07t6-0 dhVVKS']/ul/li"))
                    )
                    location_search_list=  driver.find_elements(By.XPATH, "//div[@class='LocationSearch__Container-sc-1dp07t6-0 dhVVKS']/ul/li") 
                    # Check if country is not in the list
                    not_found = any(country_name not in li.text for li in  location_search_list) 
                    
                    if not_found:    
                        print("Region/Country is not in the list.")      
                        #if unsucessfull in the current page proceed to next page
                        # Attempt to click the "Next" button
                        time.sleep(3)
                        try:
                            print("---Proceeding to the next page----")
                            next_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@class ='NavigationPanel__NextButton-sc-vkhyk2-5 kRDgoA']"))
                            )
                            time.sleep(0.4)
                            next_button.click()
                            links_click += 1
                            print(f"\nClicked Next button {links_click} times")
                            print("Successfully clicked Next Button. Navigating to the next page")
                            time.sleep(1)
                            print(f"Navigated to Page {links_click + 1}\n")
                            continue#skipping current iteration
                        except TimeoutException:
                            print("Next button not found or not clickable. Exiting loop.")
                            break   
                    else:
                        print("Region/Country is in the list.")      
                except:
                    print("Error in finding country name")
               
                print("typing country name\n")
                
                #typing the country name in the input field
                country_input.clear()
                country_input.click()#to prevent unwanted country name 
                for char in country_name:
                    
                    country_input.send_keys(char)
                    time.sleep(0.4)

                # After typing, select from dropdown
                country_input.send_keys(Keys.ARROW_DOWN)
                country_input.send_keys(Keys.ENTER)
                    
                #check if input value is the desired country/region
                try:
                    time.sleep(1)
                    element = WebDriverWait(driver,5).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@id='downshift-2-input']"))
                    )
                    
                    # Find the input element by XPath
                    input_element = driver.find_element(By.XPATH, "//input[@id='downshift-2-input']")

                    print("\nRetrieving input value for country/region location")
                    # Get the value of the input element
                    value = input_element.get_attribute("value")
                    print("\nInput element value:", value)
                    
                    if country_name == value:
                            print("---Sucessfully selected Region/Country---")
                    else:
                        print("input_element value is different")
                        print(f"The SDG you're currently in: {links_click + 1}")

                        #if unsucessfull in the current page proceed to next page
                        # Attempt to click the "Next" button
                        time.sleep(2)
                        try:
                            print("---Proceeding to the next page----")
                            next_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@class ='NavigationPanel__NextButton-sc-vkhyk2-5 kRDgoA']"))
                            )
                            time.sleep(0.5)
                            next_button.click()
                            links_click += 1
                            print(f"\nClicked Next button {links_click} times")
                            print("Successfully clicked Next Button. Navigating to the next page")
                            time.sleep(1)
                            print(f"Navigated to Page {links_click + 1}\n")
                            continue#skipping current iteration
                        except TimeoutException:
                            print("Next button not found or not clickable. Exiting loop.")
                            break    
                except Exception as e:
                    print("Can't find the input value")
                    print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
                print("Failed to select the desired country/region\n")
                
            # Selecting elements from universities
            time.sleep(2)
            try:
                # Step 2: Selecting the container for the list of universities
                #for unexpected page refresh
                max_retries = 3
                attempt = 0
                while attempt < max_retries:
                    try:
                        print("\n---Finding university container---")
                        WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='PeerSelect__Container-sc-cfs1fm-0 kNqusN']"))
                        )
                        element = driver.find_element(By.XPATH, "//div[@class='PeerSelect__Container-sc-cfs1fm-0 kNqusN']")
                        WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']"))
                        )
                        WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@class='PeerSelect__InstitutionName-sc-cfs1fm-6 jBTLtN']"))
                        )
                        print("\nFound universities container")
                        driver.execute_script("window.stop();")  # Stops current page loading
                        time.sleep(2)#allow time to load the script
                        break  # Exit loop if successful
                    except  Exception as e:
                        attempt += 1
                        print(f"Page refresh detected. Retrying... ({attempt}/{max_retries})")
                    except Exception as e:
                        raise RuntimeError("Failed to locate university container or list") from e
                
                # Select all university buttons
                time.sleep(1)
                # Step 3: Selecting all university buttons
                try:
                    element = WebDriverWait(driver, 8).until(
                            EC.presence_of_element_located((By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']/li/button"))
                        )
                    university_name_buttons = driver.find_elements(By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']/li/button")
                    university_length = len(university_name_buttons)
                    print(f"Total universities found: {university_length}")
                    print("Clicking university buttons")
                    print("Proceeding to Batch Processing\n")
                except Exception as e:
                    raise RuntimeError("Failed to retrieve university buttons") from e

                # Step 4: Process universities in batches (Batch Processing Logic)
                batch_size = 35  # Number of universities to process per batch
                click_count = 0  # Counter for clicks

                # Process universities in batches
                try:
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
                                time.sleep(0.2)  # Pause for UI responsiveness
                            except Exception as e:
                                print(f"Error clicking university button at index {index}: {e}")

                        print(f"Batch {batch_start // batch_size + 1} - Selected {click_count} universities")
                    
                        # Apply selections
                        # Step 5: Apply selections
                        time.sleep(3)
                        try:
                            print("\n---Clicking Apply button---\n")
                            apply_button = driver.find_element(By.XPATH, "//button[@class='PeerSelect__ApplyButton-sc-cfs1fm-9 frSOwt']")
                            apply_button.click()
                            print("Succesfully clicked apply button\n")
                            print("Clicking download button")
                            # Download the Excel file for the current batch
                            time.sleep(3)
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
                            print("\nAll batches processed successfully\n")
                            
                        except Exception as e:
                            print(f"Error during Apply/Table/Download steps in Batch {batch_start // batch_size + 1}: {e}")
                            #if unsucessfull in the current page proceed to next page
                            # Attempt to click the "Next" button
                            time.sleep(2)
                            try:
                                print("---Proceeding to the next page----")
                                next_button = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//button[@class ='NavigationPanel__NextButton-sc-vkhyk2-5 kRDgoA']"))
                                )
                                time.sleep(0.4)
                                next_button.click()
                                links_click += 1
                                print(f"\nClicked Next button {links_click} times")
                                print("Successfully clicked Next Button. Navigating to the next page")
                                time.sleep(1)
                                print(f"Navigated to Page {links_click + 1}\n")
                                continue#skipping current iteration
                            except TimeoutException:
                                print("Next button not found or not clickable. Exiting loop.")
                                break
                except Exception as e:
                    raise RuntimeError("Failed to process universities in batches") from e
                  
                #Step 6: Proceeding to next page     
                # Attempt to click the "Next" button
                time.sleep(3)
                try:
                    print("---Proceeding to the next page----")
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@class ='NavigationPanel__NextButton-sc-vkhyk2-5 kRDgoA']"))
                    )
                    time.sleep(0.3)
                    next_button.click()
                    links_click += 1

                    print(f"\nClicked Next button {links_click} times")
                    print("Successfully clicked Next Button. Navigating to the next page")
                    time.sleep(1)
                    print(f"Navigated to Page {links_click + 1}\n")
                except TimeoutException:
                    print("Next button not found or not clickable. Exiting loop.")
                    break     
                
                if links_click == 17:
                    print("\n---Successfully Processed all pages---")
                    print("Exiting the program in a few seconds")
                        
            except Exception as e:
                print(f"Error: {e}")
                print("Error in scraping the data. Exiting loop.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
except Exception as e:
    logging.error(f"Error in login found: {e}")
    print(driver.page_source)
finally:
    time.sleep(10)
    driver.quit()
    
