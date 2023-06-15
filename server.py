# Import flask and datetime module for showing date and time
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

import datetime

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)
client = MongoClient(
    "mongodb+srv://HARSHDALWADI:Harsh1234@cluster0.bjw1qby.mongodb.net/"
)
db = client["flaskfullstack"]
CORS(app)


# Route for seeing a data
@app.route("/data")
def get_time():
    # Returning an api for showing in reactjs
    return {"Name": "geek", "Age": "22", "Date": x, "programming": "python"}


@app.route("/users", methods=["POST", "GET"])
def data():
    if request.method == "POST":
        body = request.json
        firstName = body["firstName"]
        lastName = body["lastName"]
        emailid = body["emailid"]
        db["users"].insert_one(
            {"firstName": firstName, "lastName": lastName, "emailid": emailid}
        )
        return {
            "status": "data is posted to MongoDb",
            "firstName": firstName,
            "lastName": lastName,
            "emailid": emailid,
        }

    if request.method == "GET":
        allData = db["users"].find()
        dataJson = []
        for data in allData:
            id = data["_id"]
            firstName = data["firstName"]
            lastName = data["lastName"]
            emailid = data["emailid"]

            dataDict = {
                "id": str(id),
                "firstName": firstName,
                "lastName": lastName,
                "emailid": emailid,
            }

            dataJson.append(dataDict)

        return dataJson


@app.route("/users/<string:id>", methods=["GET", "PUT", "DELETE"])
def onedata(id):
    if request.method == "GET":
        data = db["users"].find_one({"_id": ObjectId(id)})
        id = data["_id"]
        firstName = data["firstName"]
        lastName = data["lastName"]
        emailid = data["emailid"]

        dataDict = {
            "id": str(id),
            "firstName": firstName,
            "lastName": lastName,
            "emailid": emailid,
        }

        return dataDict

    if request.method == "DELETE":
        if(ObjectId(id)):
            db["users"].delete_one({"_id": ObjectId(id)})
            return {"status": "Data id:" + id + " is deleted"}
        else:
            return {"status": "Data not exist"}

    if request.method == "PUT":
        body = request.json
        firstName = body["firstName"]
        lastName = body["lastName"]
        emailid = body["emailid"]

        db["users"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "firstName": firstName,
                    "lastName": lastName,
                    "emailid": emailid,
                }
            },
        )
        return {"status": "Data id:" + id + " is updated"}


# Running app
if __name__ == "__main__":
    app.run(debug=True)
