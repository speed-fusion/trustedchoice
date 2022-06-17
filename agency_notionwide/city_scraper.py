from playwright_driver import PlaywrightDriver
from database import Database

db = Database()

driver = PlaywrightDriver()

driver.start()

for item in list(db.states.find({"status":False}).limit(10)):
    data = []
    
    url = item["link"]
    print(url)
    driver.page.goto(url)
    soup = driver.get_soup()
    dir_list_links = soup.find("ul",{"class":"Directory-listLinks"})

    for item2 in dir_list_links.find_all("a"):
        label = item2.find("span").text
        link = "https://agency.nationwide.com" + "/" + item2.get("href")
        
        data.append({
            "city_name":label,
            "city_link":link,
            "status":False,
            "state_name":item["name"],
            "state_link":item["link"]
        })
    
    db.cities.insert_many(data)
    
    db.states.update_one(
        {"_id":item["_id"]},
        {
            "$set":{
                "status":True
            }
        }
    )


driver.stop()

# city
# 1. https://agency.nationwide.com/dc/washington