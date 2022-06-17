user = "root"
password = "C5E01228B178C925CD0A0D6C6889BB029072"
host = "localhost:27017"
database = "agency_nationwide"
import pymongo
class Database:
    def __init__(self):
        db_name = database
        connection_uri = f'mongodb://{host}/?authSource=admin'
        client = pymongo.MongoClient(connection_uri)
        db = client[db_name]
        self.states = db["states"]
        self.cities = db["cities"]
        self.companies = db["companies"]