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

import requests
from bs4 import BeautifulSoup
# from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
client = MongoClient(
    "mongodb+srv://HARSHDALWADI:Harsh1234@cluster0.bjw1qby.mongodb.net/"
)
db = client["realTimeStockData"]
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")
KILL_THREAD = False

ALL_STOCKS = []
STOCK_URL = 'https://finance.yahoo.com/quote/'


def emit_random_number(socket):
    while True:
        # num = round(random.uniform(100,200), 2)
        # print(num)
        new = livefetch(ALL_STOCKS)
        socketio.emit('live data', new)
        # print(new)
        time.sleep(5)

  
    
    # for stock in ALL_STOCKS:
    #     ALL_STOCKS_THREAD.append(threading.Thread(target=set_all_drivers, args=(stock['companyLogo'],)))
    #     ALL_STOCKS_THREAD[len(ALL_STOCKS_THREAD)-1].setDaemon = True
    #     ALL_STOCKS_THREAD[len(ALL_STOCKS_THREAD)-1].start()
    #     time.sleep(5)
    # while True:
    #     liveList = livefetch(ALL_STOCKS, ALL_STOCKS_DRIVER)
    #     socketio.emit('live list', liveList)
    #     time.sleep(2)
    #     if KILL_THREAD == True:
    #         for thread in ALL_STOCKS_THREAD:
    #             thread.join()
        
        

def current_stock_list():
    allData = db["history_data"].find({}, {'data': 0})
    print(allData)
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
    KILL_THREAD = False
    socketio.emit('hi server',{'id': request.sid})
    
    t = threading.Thread(target=emit_random_number, args=(socketio,))
    t.daemon = True
    t.start()

    

@socketio.on("disconnect")
def disconnect():
    print(request.sid)
    KILL_THREAD = True
    print('Client disconnected')

# Running app
if __name__ == "__main__":
    ALL_STOCKS = current_stock_list()
    socketio.run(app, debug = True,port = 5001)
