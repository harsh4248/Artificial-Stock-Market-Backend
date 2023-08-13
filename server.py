# Import flask and datetime module for showing date and time
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
from flask_socketio import SocketIO,emit
import threading
import random
import time
import datetime

from liveDataExample import livefetch


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
client = MongoClient(
    "mongodb+srv://HARSHDALWADI:Harsh1234@cluster0.bjw1qby.mongodb.net/"
)
db = client["realTimeStockData"]
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

ALL_STOCKS = []

def emit_random_number(socket):
    while True:
        num = round(random.uniform(100,200), 2)
        # print(num)
        socketio.emit('live data', num)

        time.sleep(2)
def emit_live_data(socket):
    while True:
        liveList = livefetch(ALL_STOCKS)
        socketio.emit('live list', liveList)
        # print('here')
        time.sleep(2)
        
        

def current_stock_list():
    allData = db["history_data"].find({}, {'data': 0})
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

def convert_data(data):
    g_list = []
    for val in data:
        # for linegraph
        # g_list.append([time.mktime(datetime.datetime.strptime(val['date'],"%Y-%m-%d").timetuple()),float(val['dayClose'])])
        # for candlestick
        
        g_list.append(
            [
                int(
                    datetime.datetime.strptime(val["date"], "%Y-%m-%d").timestamp() * 1000
                ),
                float(val["dayOpen"]),
                float(val["dayHigh"]),
                float(val["dayLow"]),
                float(val["dayClose"]),
            ]
        )
    return g_list


@app.route("/stocks", methods=["GET"])
def get_all_stock():
    if request.method == "GET":
        
        return ALL_STOCKS


@app.route("/stocks/<string:id>", methods=["GET"])
def single_stock_data(id):
    if request.method == "GET":
        data = db["history_data"].find_one({"_id": ObjectId(id)})
        convert_data(data["data"])
        return {
            "_id": str(data["_id"]),
            "companyLogo": data["companyLogo"],
            "companyName": data["companyName"],
            "price": data["price"],
            "volume": data["volume"],
            "marketCap": data["marketCap"],
            "historical_data": convert_data(data["data"]),
        }

@socketio.on("connect")
def connected():
    print(request.sid)
    print("Client is Connected")
    socketio.emit('hi server',{'id': request.sid})

    t = threading.Thread(target=emit_live_data, args=(socketio,))
    t.daemon = True
    t.start()

    

@socketio.on("disconnect")
def disconnect():
    print(request.sid)
    print('Client disconnected')

# Running app
if __name__ == "__main__":
    ALL_STOCKS = current_stock_list()
    socketio.run(app, debug = True,port = 5001)
