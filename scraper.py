# Web scraper for kijiji auto

# 1 Necessary imports
from selenium import webdriver
import mysql.connector
import time

# 2 Open the chromedriver and set the current height of the window
driver = webdriver.Chrome("chromedriver")
driver.get('https://www.kijijiautos.ca/fr/voitures/#od=down&sb=ct')
last_height = driver.execute_script("return document.body.scrollHeight")


myList = open("vehicleID.txt").readlines()
# 3 Stop the webscraping if we have 100 000 vehicle ids or more
while len(myList) < 100000:
    time.sleep(2)
    SearchResultListItems = driver.find_elements_by_css_selector('div[data-testid="VehicleListItem"]')
    
    vehicleIdFileWrite = open('vehicleID.txt', 'a')

    for resultItem in SearchResultListItems:
        vehicleId =  resultItem.get_attribute("data-test-ad-id")
        vehicleId = vehicleId + '\n'
        if vehicleId in myList:
            print(vehicleId, 'already in file')
        else:
            vehicleIdFileWrite.write(vehicleId)
            myList.append(vehicleId)
            print(vehicleId, 'INSERTED')

    vehicleIdFileWrite.close()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break

    last_height = new_height

    print('number of vehicle IDS', len(myList))

driver.close()
