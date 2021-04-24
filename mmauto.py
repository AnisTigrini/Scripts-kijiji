# 1 Get all brands and models for cars on kijiji auto
from selenium import webdriver
import mysql.connector
import time

# 2 Get driver connection and cursor going
driver = webdriver.Chrome("chromedriver")
connection = mysql.connector.connect(host='127.0.0.1',
                             user='root',
                             password='****',
                             database='jikiki',
                             charset='utf8mb4')

driver.get('https://www.kijijiautos.ca/')
mycursor = connection.cursor()

# 3 Find all the brands and models tags
time.sleep(130)
element = driver.find_element_by_id("model")
brandTags = element.find_elements_by_css_selector("optgroup")
brandAndModelList = []

for brandTag in brandTags:
    brandName = brandTag.get_attribute("label")

    modelTags = brandTag.find_elements_by_tag_name('option')

    for modelTag in modelTags:
        modelName = modelTag.get_attribute("innerHTML")
        brandAndModelList.append((brandName, modelName))

# 4 Insert all the data and close the connection to the webdriver
sql = "INSERT INTO mmauto (Marque, Modele) VALUES (%s, %s)"
mycursor.executemany(sql, brandAndModelList)
connection.commit()
print(mycursor.rowcount, "was inserted.")
driver.close()
