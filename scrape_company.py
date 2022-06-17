import json
import time
from playwright_driver import PlaywrightDriver


driver = PlaywrightDriver()

driver.start()

cities = None

with open("city.json","rb") as f:
    cities = json.load(f)

base_url = "https://www.trustedchoice.com"

company_links = []

for city in cities:
    print(city)
    
    city_url = base_url + city["city_url"]
    
    driver.page.goto(city_url)
    
    soup = driver.get_soup()
    
    for link in soup.find_all("a",{"class":"agency-directory-profile-button btn btn-sm btn-outline-secondary stretched-link-override"}):
        c_link = link.get("href")
        
        tmp = city.copy()
        tmp["company_link"] = c_link
        company_links.append(tmp)
        print(c_link)

with open("companies.json","w") as f:
    f.write(json.dumps(company_links))
    
driver.stop()