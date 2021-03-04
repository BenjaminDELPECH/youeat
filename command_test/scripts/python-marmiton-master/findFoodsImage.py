import requests
import json


createLMFQuery = """
{
    foods{
        id
        nameFr
    }
}
"""




def sendQueryToDjangoAPI(query, payload, objPropResult):
    url = 'http://127.0.0.1:8888/graphql/'
    r = requests.post(url, json={'query': query, 'variables': payload})
    return json.loads(r.text)['data'][objPropResult]

from selenium import webdriver
import time

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ennov",
  database="simplenutrition"
)


def executeSQLRequest(sql_req, variables,insert):
    
    mycursor = mydb.cursor()
    if variables:
        mycursor.execute(sql_req, variables)
    else:
        mycursor.execute(sql_req)
    if not insert:
        return mycursor.fetchall()
    else:
        mydb.commit()
        mycursor.close()



try:


    DRIVER_PATH = 'C:/dev/runtime/chromedriver_win32_chrome_87/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.set_page_load_timeout(10)

    foods = executeSQLRequest("""
    SELECT * from foods_food where id not in (
    Select food_id from foods_foodimage
    )
    """, None, False)
    for food in foods:
        food_name = food[2]
        food_id = food[0]
        driver.get("https://www.google.com/search?q={}&tbm=isch&ved=2ahUKEwjGz_aKtY3uAhUlgXMKHZP0CmoQ2-cCegQIABAA&oq=banane&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgQIABBDMgUIABCxAzICCAAyBQgAELEDMgIIADICCAAyAggAMgIIADoHCCMQ6gIQJzoECCMQJzoHCAAQsQMQQ1CsBljRD2CxEGgBcAB4AIABQogB5wKSAQE2mAEAoAEBqgELZ3dzLXdpei1pbWewAQq4AQPAAQE&sclient=img&ei=neD4X4aNKKWCzgOT6avQBg&bih=937&biw=1920&rlz=1C1CHBF_frFR930FR930".format(food_name))
        time.sleep(0.3)
        foods_images = driver.find_elements_by_tag_name('img')
        print(food_name)
        first_image = foods_images[0].get_attribute('src')
        payload = {"foodId": int(food[0]), "image": first_image}
        variables = (food_id,first_image)
        executeSQLRequest("""
            INSERT INTO foods_foodimage (food_id, image)
    values (%s, %s);
        """, variables, True)

except Exception:
    print("error")


