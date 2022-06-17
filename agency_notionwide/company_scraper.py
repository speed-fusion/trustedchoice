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

while True:
    driver = PlaywrightDriver()

    driver.start()

    for item in list(db.cities.find({"status":False}).limit(10)):
        try:
            data = []
            
            url = item["city_link"]
            print(url)
            driver.page.goto(url)
            soup = driver.get_soup()
            dir_list_links = soup.find("div",{"class":"Directory-content"})

            for item2 in dir_list_links.find_all("li"):
                try:
                    a_tag = item2.find("a")
                    
                    label = a_tag.find("h3").text
                    link = "https://agency.nationwide.com" + a_tag.get("href").strip(".")
                    
                    tmp = item.copy()
                    del tmp["_id"]
                    tmp["company_name"] = label
                    tmp["company_link"] = link
                    
                    # print(tmp)
                    # continue
                    data.append(tmp)
                except Exception as e:
                    print(f'error:{str(e)}')
            # continue
            db.companies.insert_many(data)
            
            db.cities.update_one(
                {"_id":item["_id"]},
                {
                    "$set":{
                        "status":True
                    }
                }
            )
        except Exception as e:
            print(f'error : {str(e)}')
            


    driver.stop()

# city
# 1. https://agency.nationwide.com/dc/washington