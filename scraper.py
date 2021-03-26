#1 Web scraper for kijiji auto
from selenium import webdriver
import mysql.connector
import time

driver = webdriver.Chrome("chromedriver")


driver.get('https://www.kijijiautos.ca/fr/voitures/#od=down&sb=ct')

time.sleep(10)

driver.close()
