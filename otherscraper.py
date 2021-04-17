# Web scraper for kijiji auto
# 1 Necessary imports
from platform import version
from mysql.connector.errors import Error
from selenium import webdriver
import mysql.connector
import time

# 2 Open the chromedriver and set the current height of the window
driver = webdriver.Chrome("chromedriver")

connection = mysql.connector.connect(host='127.0.0.1',
                             user='root',
                             password='4991',
                             database='jikiki',
                             charset='utf8mb4')

mycursor = connection.cursor()
vehicleIdFileWrite = open('vehicle.txt', 'a')

for vid in open("vehicleID.txt").readlines():
    driver.get('https://www.kijijiautos.ca/fr/voitures/#vip={}'.format(vid))
    
    #2.1 Some variable we will need
    idPost = vid
    if ("\n") in idPost:
        idPost = idPost.strip("\n")
    if ("\r") in idPost:
        idPost = idPost.strip("\r")
    if ("\t") in idPost:
        idPost = idPost.strip("\t")
    if (" ") in idPost:
        idPost = idPost.strip(" ")
    title = None
    price = None
    description = None
    state = 'Usagé'
    kilos = 0
    autoversion = '-'
    transmission = 'Automatique'
    motricity = '-'
    gaz = 'Autres'
    brand = '-'
    model = '-'
    carType = '-'
    year = 1990
    equipments = []
    imageLinks = []

    # 2.2 Click this element
    try:
        divElement = driver.find_element_by_css_selector('div[data-testid="HashedVipDetailLink"]')
        buttonToClick = divElement.find_element_by_css_selector('button')
        buttonToClick.click()
    except:
        print('Error finding the button element!')

    time.sleep(4)

    # 3 Get the available photos on the website
    try:
        buttonElement = driver.find_elements_by_css_selector('button[data-testid="TeaserImage"]')
        
        for element in buttonElement:
            imageLink = element.find_element_by_css_selector('img').get_attribute('src')
            imageLinks.append(imageLink)
        
        print(imageLinks)

    except:
        print('Error finding images')


    # 4 Get the title of the post
    try:
        # There is only one h1 tag and it is for the title of the post
        title = driver.find_element_by_css_selector('h1').get_attribute("innerHTML")
        print(title)

    except:
        print('Error finding title')


    # 5 Get the price of the vehicle
    try:
        # There is only one h1 tag and it is for the title of the post
        priceElement = driver.find_element_by_css_selector('span[data-testid="listing-basic-info-section-price"]')
        price = priceElement.find_element_by_css_selector('span').get_attribute("innerHTML")
        price = price.replace('&nbsp;', '')
        price = price.strip('$')
        price = int(price)
        print('prix', price)

    except:
        print('Error finding price')


    # 6 Get the description of the post
    try:
        # There is only one h1 tag and it is for the title of the post
        descriptionElement = driver.find_element_by_css_selector('section[data-testid="ListingDescriptionSection"]')
        description = descriptionElement.find_element_by_css_selector('span').get_attribute("innerHTML")
        print(description)

    except:
        print('Error finding title')


    # 8 Get extra information
    try:
        listTagElement = driver.find_element_by_css_selector('ul[data-testid="quickFact"]')
        listElements = listTagElement.find_elements_by_css_selector('li')

        for listElement in listElements:
            listElement = listElement.find_elements_by_css_selector('span')

            try:
                if listElement[1].get_attribute('innerHTML') == 'État':
                    state = listElement[0].get_attribute('innerHTML')

                elif listElement[1].get_attribute('innerHTML') == 'Kilomètres':
                    kilos = listElement[0].get_attribute('innerHTML')
                    kilos = kilos.replace('&nbsp;', '')
                    kilos = kilos.strip('km')
                    kilos = int(kilos)
                
                elif listElement[1].get_attribute('innerHTML') == 'Transmission':
                    transmission = listElement[0].get_attribute('innerHTML')

                elif listElement[1].get_attribute('innerHTML') == 'Version':
                    autoversion = listElement[0].get_attribute('innerHTML')
                
                elif listElement[1].get_attribute('innerHTML') == 'Motricité':
                    motricity = listElement[0].get_attribute('innerHTML')

                elif listElement[1].get_attribute('innerHTML') == 'Type de carburant':
                    gaz = listElement[0].get_attribute('innerHTML')
            
            except Error as e:
                print(e)
        
        print('- etat', state)
        print('- kilos' ,kilos)
        print('version' ,autoversion)
        print('transmission', transmission)
        print('motricité', motricity)
        print('type carburant', gaz)

    except:
        print('Error finding extra information')


    # 9 Get important details about the car

    try:
        previewElement = driver.find_element_by_css_selector('div[data-testid="section0"]')
        listElements = previewElement.find_elements_by_css_selector('li')

        for el in listElements:
            el = el.find_elements_by_css_selector('span')

            try:
                if el[0].get_attribute('innerHTML') == 'Marque: ':
                    brand = el[1].get_attribute('innerHTML')

                elif el[0].get_attribute('innerHTML') == 'Modèle: ':
                    model = el[1].get_attribute('innerHTML')

                elif el[0].get_attribute('innerHTML') == 'Année: ':
                    year = el[1].get_attribute('innerHTML')

                elif el[0].get_attribute('innerHTML') == 'Type de carrosserie: ':
                    carType = el[1].get_attribute('innerHTML')  

            except Error as e:
                print(e)

        print('marque', brand)
        print('model', model)
        print('annee', year)
        print('Type carrosserie', carType)

    except:
        print('Error on getting the important details')


    # 10 Get the equipment
    try:
        equipmentElement = driver.find_element_by_css_selector('div[data-testid="section1"]')
        listElements = equipmentElement.find_elements_by_css_selector('li')

        for el in listElements:
            equipment = el.find_element_by_css_selector('span').get_attribute('innerHTML')
            equipments.append(equipment)

        print(equipments)

    except:
        print('Error on getting the equipment')


    try:
        if title != None and price != None and description != None and len(imageLinks) >= 3:
            mycursor.execute("CALL entrerPost('{}', '{}', '{}', {}, '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(idPost, "philippefortin@gmail.com", title, price, description, state, kilos, "-", transmission, "-", gaz, carType, brand, model, year,imageLinks[0], imageLinks[1], imageLinks[2], "bluetooth", "AC", "radio", "telephone"))

    except Error as e:
        print(e)
driver.close()