import json
import time
from playwright_driver import PlaywrightDriver
from database import Database

db = Database()

driver = PlaywrightDriver()

driver.start()

url = "https://agency.nationwide.com"

driver.page.goto(url)

soup = driver.get_soup()

dir_list_links = soup.find("ul",{"class":"Directory-listLinks"})

data = []

for item in dir_list_links.find_all("a"):
    label = item.find("span").text
    link = url + "/" + item.get("href")
    
    data.append({
        "name":label,
        "link":link,
        "status":False
    })
    

db.states.insert_many(data)

driver.stop()