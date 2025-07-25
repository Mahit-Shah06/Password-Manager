import pymongo
import certifi

class DataBase:
    def __init__(self):
        mongo_var = "mongodb+srv://Superrr:WKIwYy5aCOi3jJLn@pswdmgrdb.7dx5krf.mongodb.net/?retryWrites=true&w=majority&appName=PswdMgrDB"
        client = pymongo.MongoClient(mongo_var, tlsCAFile=certifi.where())
        self.db = client['password_manager']
        self.user_collection = self.db['passwords']

    def check_if_public_key_exists(self, public_key: str) -> bool:
        collection_names = self.db.list_collection_names()
        for i in collection_names: print(i)
        if public_key in collection_names:
            return False

    def add_data(self, data, public_key):
        self.user_collection = self.db[public_key]
        data_entry = {
            "website" : data[0],
            "email" : data[1],
            "password" : data[2],
            "notes" : data[3]
        }
        self.user_collection.insert_one(data_entry)

    def fetch_data(self, public_key ):
        self.user_collection = self.db[public_key]
        stored_data = self.user_collection.find({})
        return list(stored_data)

    # if __name__ == "__main__":
    #     try:
    #         # The ping command is a simple way to test the connection
    #         client.admin.command('ping')
    #         print("MongoDB connection successful!")
    #     except Exception as e:
    #         print(f"Connection failed: {e}")