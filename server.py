# Import flask and datetime module for showing date and time
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

import time
import datetime

app = Flask(__name__)
client = MongoClient(
    "mongodb+srv://HARSHDALWADI:Harsh1234@cluster0.bjw1qby.mongodb.net/"
)
db = client["realTimeStockData"]
CORS(app)

def convert_data(data):
    g_list = []
    for val in data:
        g_list.append([time.mktime(datetime.datetime.strptime(val['date'],"%Y-%m-%d").timetuple()),float(val['dayClose'])])
    return g_list
@app.route("/stocks", methods=["GET"])
def get_all_stock():
    if request.method == "GET":
        allData = db["history_data"].find()
        dataJson = []
        for data in allData:
            dataJson.append(
                {
                    "_id": str(data["_id"]),
                    "companyLogo": data["companyLogo"],
                    "companyName": data["companyName"],
                    "price": data["price"],
                    "volume": data["volume"],
                    "marketCap": data["marketCap"],
                }
            )

        return dataJson
    
@app.route('/stocks/<string:id>', methods = ['GET'])
def single_stock_data(id):

    if(request.method == 'GET'):
        data = db['history_data'].find_one({'_id' : ObjectId(id)})
        convert_data(data['data'])
        return {'_id' : str(data['_id']),
                'companyLogo': data['companyLogo'],
                'companyName': data['companyName'],
                'price': data['price'],
                'volume': data['volume'],
                'marketCap': data['marketCap'],
                'historical_data' : convert_data(data['data'])}

    


# Running app
if __name__ == "__main__":
    app.run(debug=True)
