import requests
from bs4 import BeautifulSoup
from lxml import etree
# from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import random
import time

import aiohttp
import asyncio
import threading


URL = 'https://finance.yahoo.com/quote'

def getStockLivePrice(stock,results):
    companyLogo = stock['companyLogo']
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options = option)
    
    try: 
        url = URL + '/'+ companyLogo + '?' + 'p='+companyLogo
        print(url)
        driver.get(url)

        # time.sleep(5)
        price = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,'//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]'))).text
        # live_stream_div= driver.find_element(By.XPATH, '//*[@id="quote-header-info"]')
        # live_stream_tag = live_stream_div.find_elements(By.TAG_NAME, 'fin-streamer')
        # price = live_stream_tag[0].text

        stock['price'] = round(float(price), 2)
        # print('stock List = ',stock)
        results.append(stock)
    except Exception as e:
        print(e)

    finally: 
        driver.quit()
    
    


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

    # async with aiohttp.ClientSession() as session:
    #     tasks = [getStockLivePrice(session, stock) for stock in stockList]
    #     result = await asyncio.gather(*tasks)
    
    # return result
    results = []
    threads = [threading.Thread(target=getStockLivePrice, args=(stock,results), daemon=True) for stock in stockList]

    for thread in threads:
        thread.daemon = True
        thread.start()
    # time.sleep(10)
    for thread in threads:
        thread.join()
    print(results)
    return results
    # stockListCopy = stockList[:]
    # for stock in stockListCopy:
    #     stock['price'] = getStockLivePrice(stock['companyLogo'])

    # return stockListCopy
# def livefetch(stockList, allDrivers):

    
    print(allDrivers)
    for stock in stockList:
        # driver = allDrivers[stock['companyLogo']]
        # stock['price'] = driver.find_element(By.XPATH, '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]').text
        try:
            driver = allDrivers[stock['companyLogo']]
            stock['price'] = driver.find_element(By.XPATH, '//*[@id="quote-header-info"]/div[3]/div[1]/div[2]/fin-streamer[2]').text
        except BaseException as e:
            print(e)
    return stockList

