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

# db.companies.insert_many(companies)

db.companies.update_many({},{"$set":{"status":0}})


