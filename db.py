import pymongo
import certifi

class DataBase:
    def __init__(self):
        try:
            mongo_url = "mongodb+srv://Superrr:FryBrUFd1Ka9wU0q@pswdmgrdb.7dx5krf.mongodb.net/?retryWrites=true&w=majority&appName=PswdMgrDB"
            self.client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where(), serverSelectionTimeoutMS = 5000)
            self.db = self.client['password_manager']
            self.user_collection = self.db['passwords']
            print("✅ Connected to MongoDB successfully!")
        except Exception as e:
            print("❌ Connection failed:", e)

    def check_if_public_key_exists(self, public_key: str) -> bool:
        collection_names = self.db.list_collection_names()
        for i in collection_names: print(i)
        return public_key in collection_names

    def add_data(self, data, public_key):
        if not self.db:
            return False, "Database not connected"
        try:
            self.user_collection = self.db[public_key]
            data_entry = {
                "website" : data[0],
                "email" : data[1],
                "password" : data[2],
                "notes" : data[3]
            }
            self.user_collection.insert_one(data_entry)
            return True, "Data added successfully"
        except Exception as e:
            return False, f"Error {e}"

    def fetch_data(self, public_key ):
        if not self.db:
            return []
        try:
            self.user_collection = self.db[public_key]
            stored_data = self.user_collection.find({})
            return list(stored_data)
        except Exception as e:
            return False, f"Error {e}"

# uri = "mongodb+srv://Superrr:FryBrUFd1Ka9wU0q@pswdmgrdb.7dx5krf.mongodb.net/?retryWrites=true&w=majority&appName=PswdMgrDB"

# try:
#     client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
#     client.admin.command('ping')
#     print("✅ Connected to MongoDB successfully!")
# except Exception as e:
#     print("❌ Connection failed:", e)