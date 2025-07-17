import pymongo

mongo_var = "mongodb+srv://Superrr:YlGV7cV7mek8RtJa@passwordmanagerdb.oynnbfo.mongodb.net/?retryWrites=true&w=majority&appName=PasswordManagerDB"

client = pymongo.MongoClient(mongo_var)

db = client['password_manager']
collection = db['passwords']

def add_data(data):
    data_entry = {"website" : data[0],
                  "email" : data[1],
                  "password" : data[2],
                  "notes" : data[3]}
    collection.insert_one(data_entry)
    print("Data added successfully.")