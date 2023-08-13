from pymongo import MongoClient
import os
import csv
import time

def send_data_mongo(data):
    client = MongoClient(
        "mongodb+srv://HARSHDALWADI:Harsh1234@cluster0.bjw1qby.mongodb.net/"
    )
    db = client["realTimeStockData"]
    collection = db["history_data"]

    result = collection.insert_one(data)

    print("Inserted Id: ", result.inserted_id)

    client.close()

def get_history_from_csv(file):
    data = []
    with open(file, "r") as csvfile:
        csvreader = csv.reader(csvfile)

        fields = next(csvreader)

        for row in csvreader:
            data.append(
                {
                    "date": row[0],
                    "dayOpen": row[1],
                    "dayHigh": row[2],
                    "dayLow": row[3],
                    "dayClose": row[4],
                }
            )
    return data

def read_all_files():
    
    pass

# TODO 1: READ SRC FOLDER AND ALL FILES FROM IT
# TODO 2: MAKE LIST OF WHOLE HISTORY DATA
# TODO 3: FIND THAT DATA IN MONGODB AND SEND TO IT.