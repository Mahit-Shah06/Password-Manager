import pymongo
import certifi

class DataBase:
    def __init__(self):
        mongo_var = "mongodb+srv://Superrr:YlGV7cV7mek8RtJa@passwordmanagerdb.oynnbfo.mongodb.net/?retryWrites=true&w=majority&appName=PasswordManagerDB"
        client = pymongo.MongoClient(mongo_var, tlsCAFile=certifi.where())
        db = client['password_manager']
        self.user_collection = db['passwords']

    def add_data(self, data):
        data_entry = {"website" : data[0],
                    "email" : data[1],
                    "password" : data[2],
                    "notes" : data[3]}
        self.user_collection.insert_one(data_entry)

    def fetch_data(self):
        store_data = self.user_collection.find({})
        return list(store_data)

    # if __name__ == "__main__":
    #     try:
    #         # The ping command is a simple way to test the connection
    #         client.admin.command('ping')
    #         print("MongoDB connection successful!")
    #     except Exception as e:
    #         print(f"Connection failed: {e}")