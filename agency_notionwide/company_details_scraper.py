import json
import time
from playwright_driver import PlaywrightDriver
from database import Database

db = Database()

# unique = {}

# cities = list(db.cities.find({}))

# print(len(cities))

# for c in cities:
#     unique[c["city_link"]] = 1

# print(len(unique))

# while True:

def extract_company_details(soup):
    
    phone_number = soup.find("span",{"itemprop":"telephone"})
    if phone_number != None:
        phone_number = phone_number.text.strip(":").strip()
    
    email = soup.find("div",{"class":"Core-emailWrapper"})
    
    if email != None:
        email = email.find("a")
        if email != None:
            email = email.get("href").split(":")[-1]
    
    products = []
    
    core_products = soup.find("div",{"class":"Core-products"})
    if core_products != None:
        for li in core_products.find_all("li"):
            products.append(li.text)
    
    street = soup.find("meta",{"itemprop":"streetAddress"})
    
    if street != None:
        street = street.get("content")
    
    postcode = soup.find("span",{"itemprop":"postalCode"})
    
    if postcode != None:
        postcode = postcode.text
    
    full_address = soup.find("address",{"itemprop":"address"})
    if full_address != None:
        full_address = full_address.text.strip()
    
    return {
        "phone_number":phone_number,
        "email":email,
        "products":products,
        "street":street,
        "postcode":postcode,
        "full_address":full_address
    }


while True:

    driver = PlaywrightDriver()

    driver.start()

    for item in list(db.companies.find({"status":False}).limit(10)):
        try:
            url = item["company_link"]
            print(url)
            driver.page.goto(url)
            soup = driver.get_soup()
            
            data = extract_company_details(soup)
            
            data["status"] = 0
            
            # continue
            db.companies.update_one(
                {"_id":item["_id"]},
                {
                    "$set":data
                }
            )
        except Exception as e:
            print(f'error : {str(e)}')
            
            db.companies.update_one(
                {"_id":item["_id"]},
                {
                    "$set":{
                        "error_count":0
                    }
                }
            )
            
        
    driver.stop()

# city
# 1. https://agency.nationwide.com/dc/washington