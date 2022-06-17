import json
import time
from playwright_driver import PlaywrightDriver

user = "root"
password = "C5E01228B178C925CD0A0D6C6889BB029072"
host = "localhost:27017"
database = "trusted_choice"
import pymongo
import json
class Database:
    def __init__(self):
        db_name = database
        connection_uri = f'mongodb://{host}/?authSource=admin'
        client = pymongo.MongoClient(connection_uri)
        db = client[db_name]
        
        self.companies = db["companies"]

db = Database()



companies = None

base_url = "https://www.trustedchoice.com"

with open("companies.json","rb") as f:
    companies = json.load(f)
    
print(len(companies))
    
    
driver = PlaywrightDriver()

def extract_agency_website(soup):
    try:
        url = soup.find("div",{"id":"agency-profile-header-details"}).find("a",{"target":"_blank"}).get("href")
        return url
    except:
        return None

while True:
    driver.start()
    companies = list(db.companies.find({"status":2,"home_insurance":0,"auto_insurance":0}).limit(100))
    for company in companies:
        print(company)
        company_url = base_url + company["company_link"]
        print(company_url)
        agency_website = company["agency_website"]
        auto_insurance = 0
        home_insurance = 0
        if agency_website != None:
            
            try:
                driver.page.goto(agency_website)
                
                soup = driver.get_soup()
                
                html_text = soup.text.strip().lower()
                
                if "automobile" in html_text:
                    auto_insurance = 1
                    
                if "homes" in html_text:
                    home_insurance = 1
                
                print(f'auto_insurance : {auto_insurance}')
                print(f'home_insurance : {home_insurance}')
            except Exception as e:
                print(str(e))
                
        db.companies.update_one(
            {"_id":company["_id"]},
            {
                "$set":{
                    "status":3,
                    "auto_insurance":auto_insurance,
                    "home_insurance":home_insurance
                }
            }
        )
    driver.stop()