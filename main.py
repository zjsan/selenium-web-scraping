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

    #selecting element from universities
    try:
        #selecting the container for the list of university
        element = driver.find_element(By.XPATH, "//div[@class = 'PeerSelect__Container-sc-cfs1fm-0 kNqusN']")
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']"))
            )
        WebDriverWait(driver,10).until(
           EC.presence_of_element_located((By.XPATH, "//span[@class='PeerSelect__InstitutionName-sc-cfs1fm-6 jBTLtN']"))
           )
        print("\nfound universities\n")
        
        try:
            # Step 1: Remove Selection Limit via JavaScript
            # Find the element with data-testid='selected-number' 
            # Execute JavaScript to remove the selection limit 
            # Find the element with data-testid='selected-number' 
            element = driver.find_element(By.XPATH, "//button[@class ='PeerSelect__Tab-sc-cfs1fm-2 cKpits']") # Execute JavaScript to manipulate or remove the selection limit 
            # Example: Remove the element from the DOM 
            driver.execute_script("""
                const maxSelectionLimit = 1000;
                const limitElement = document.querySelector('[data-testid="selected-number"]');

                if (limitElement) {
                    console.log('Found limit element:', limitElement.innerText);

                    const parent = limitElement.closest('[data-testid]');
                    if (parent) {
                        parent.setAttribute('data-max', maxSelectionLimit);
                        console.log('Modified selection limit to:', maxSelectionLimit);
                    }

                    // Overwrite event listeners or limit-enforcing functions
                    //alert('Selection bypassed.');
                    //alert('Event listeners modified.');
                }
            """)#sucessfully removed the element but limitr restriction still exist
            # Assuming an alert pops up after a certain action
           # alert = Alert(driver)
            #alert.accept()
            print('Selection bypassed.')
            print('Event listeners modified.')
            time.sleep(1)  # Allow time for the changes to take effect

            print("----sucess removing limit restriction----")
            
            
            #selecting the list elements that contains the names of the universities ---- website has a limit in selecting number of universities, need to fix it
            try:
                countryitem = driver.find_elements(By.XPATH, "//ul[@class='PeerSelect__ListContainer-sc-cfs1fm-3 dVJxfI']/li/button")
                country_length = len(countryitem)
                countryitem_button = driver.find_elements(By.XPATH,"//button[@class='PeerSelect__ListItemButton-sc-cfs1fm-4 caXFaO']")
                
                
                #testing if all countries are selected
                click_count = 0#counter for how many times the university's button clicked
                for item in range(country_length):
                    print(countryitem[item].text)
                    
                    #making the button click faster to select all universities in the list 
                    print("\n\n----checking university names via button---")
                    try:
                        countryitem_button[item].click()
                        print(countryitem_button[item].text)
                        click_count += 1
                        continue
                    except:
                        break
                print("----Universities are printed----\n")
                print("Button was clicked: " + str(click_count) + " times")
            except Exception as e:
                print(f"Error: {e}")
                print("error on clicking university buttons")  
            
        except Exception as e:
            print(f"Error: {e}")
            print("Can't remove selection restriction")
            
    except Exception as e:
        print(f"Error: {e}")
        print("error fetching universities")
        
    #going to next part
    #clicking the APPLY button
    apply_button = driver.find_element(By.XPATH, "//button[@class='PeerSelect__ApplyButton-sc-cfs1fm-9 frSOwt']")
    apply_button.click()
    
    table_button = driver.find_element(By.XPATH,"//button[@class='TabSelector__Tab-sc-x9oxnj-1 zLZxw']")
    table_button.click()
    
    # #next step clicking download button
    # download = driver.find_element(By.XPATH, "//button[@class='DownloadButton__TriggerButton-sc-plxomw-1 bTWVdx']")
    # download.click()
    
    #clicking download excel file
    # element = WebDriverWait(driver,3).until(
    #     EC.presence_of_element_located((By.XPATH, "//button[@class='DownloadButton__Download-sc-plxomw-4 hDjlSG']"))
    # )
    # download_excel = driver.find_element(By.XPATH, "//button[@class='DownloadButton__Download-sc-plxomw-4 hDjlSG']")
    # download_excel.click()
    print("\nScrapping Done")
except Exception as e:
    logging.error(f"Error in login found: {e}")
    print(driver.page_source)
finally:
    time.sleep(90)
    driver.quit()
    
