import pymongo
import certifi

mongo_var = "mongodb+srv://Superrr:YlGV7cV7mek8RtJa@passwordmanagerdb.oynnbfo.mongodb.net/?retryWrites=true&w=majority&appName=PasswordManagerDB"

client = pymongo.MongoClient(mongo_var, tlsCAFile=certifi.where())

db = client['password_manager']
collection = db['passwords']

def add_data(data):
    data_entry = {"website" : data[0],
                  "email" : data[1],
                  "password" : data[2],
                  "notes" : data[3]}
    collection.insert_one(data_entry)
    print("Data added successfully.")

if __name__ == "__main__":
    try:
        # The ping command is a simple way to test the connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")