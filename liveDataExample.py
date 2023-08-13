import requests
from bs4 import BeautifulSoup
# from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import random

import time
# URL + / companyLogo + ? + p = companyLogo

URL = 'https://finance.yahoo.com/quote'

def getStockLivePrice(companyLogo):
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options = options)
    # driver.get(URL + '/'+ companyLogo + '?' + 'p='+companyLogo)

    

    return round(random.uniform(100,200), 2)
def livefetch(stockList):

    # url = 'https://www.marketwatch.com/investing/index/adow?countrycode=xx&mod=asia-market-data'

    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(options = options)
    # driver.get(url)

    # time.sleep(5)

    
    # i = 0
    # while(True):
    #     stock_price = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div[3]/div/div[2]/h2/bg-quote')
    #     print(stock_price.text)
    #     time.sleep(5)
    #     i += 1
    #     if(i == 100):
    #         break

    # driver.close()
    for stock in stockList:
        stock['price'] = getStockLivePrice(stock['companyLogo'])

    return stockList

