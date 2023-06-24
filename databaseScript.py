import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
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


def get_history(link_url, driver):
    # link_text = link.text
    # link_url = link.get_attribute("href")
    # These helps to basically click on the link
    driver.get(link_url)
    # Finding nav bar to go on historical tab.
    nav_bar = driver.find_element(By.ID, "quote-nav")
    all_a = nav_bar.find_elements(By.TAG_NAME, "a")

    # Now we are in the historical tab so we will access the tab
    driver.get(all_a[5].get_attribute("href"))

    # here we get historical data now we have click on max so that we get max data range.
    table = driver.find_element(By.ID, "Col1-1-HistoricalDataTable-Proxy")

    table_range_btn = table.find_element(By.CLASS_NAME, "dateRangeBtn")

    table_range_btn.click()
    viewbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "dropdown-menu"))
    )

    drop_down_uls = viewbox.find_elements(By.TAG_NAME, "ul")
    # print(drop_down_uls)
    li_btns = drop_down_uls[1].find_elements(By.TAG_NAME, "li")
    li_btns[3].click()
    # drop_down.find_elements(By.TAG_NAME,'ul')
    print(table_range_btn.text)

    # apply_btn = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='Bgc($linkColor)']"))
    # )
    # driver.switch_to.default_content()
    # viewbox.send_keys(Keys.RETURN)

    apply_btn = table.find_element(By.TAG_NAME, "button")
    print(apply_btn.text)
    apply_btn.click()

    time.sleep(5)

    # elements = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located(
    #         (
    #             By.XPATH,
    #             "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/tbody/tr",
    #         )
    #     )
    # )
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(driver.execute_script("return document.body.scrollHeight"))
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll the page and wait for new data to load
    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")

        # Wait for a short delay to allow new data to load
        time.sleep(2)  # Adjust the delay as needed

        # Get the new page height after scrolling
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Check if the page height has changed
        if new_height == last_height:
            # No more data loaded, exit the loop
            break
        # Update the last height
        last_height = new_height
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table")

    data = []
    for row in table.tbody.find_all("tr"):
        columns = row.find_all("td")

        if columns != []:
            data.append(
                {
                    "date": columns[0].text,
                    "dayOpen": columns[1].text,
                    "dayHigh": columns[2].text,
                    "dayLow": columns[3].text,
                    "dayClose": columns[4].text,
                }
            )
    # for element in elements:
    #     columns = element.find_elements(By.TAG_NAME, "td")
    #     if columns != []:
    #         data.append(
    #             {
    #                 "date": columns[0].text,
    #                 "dayOpen": columns[1].text,
    #                 "dayHigh": columns[2].text,
    #                 "dayLow": columns[3].text,
    #                 "dayClose": columns[4].text,
    #             }
    #         )
    print("here", len(data))
    return data


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


def download_csv(url, driver):
    driver.get(url)

    # Finding nav bar to go on historical tab.
    nav_bar = driver.find_element(By.ID, "quote-nav")
    all_a = nav_bar.find_elements(By.TAG_NAME, "a")

    # Now we are in the historical tab so we will access the tab
    driver.get(all_a[5].get_attribute("href"))

    # here we get historical data now we have click on max so that we get max data range.
    table = driver.find_element(By.ID, "Col1-1-HistoricalDataTable-Proxy")

    table_range_btn = table.find_element(By.CLASS_NAME, "dateRangeBtn")

    table_range_btn.click()
    viewbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "dropdown-menu"))
    )

    drop_down_uls = viewbox.find_elements(By.TAG_NAME, "ul")
    # print(drop_down_uls)
    li_btns = drop_down_uls[1].find_elements(By.TAG_NAME, "li")
    li_btns[3].click()
    # drop_down.find_elements(By.TAG_NAME,'ul')
    print(table_range_btn.text)

    # apply_btn = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class^='Bgc($linkColor)']"))
    # )
    # driver.switch_to.default_content()
    # viewbox.send_keys(Keys.RETURN)

    apply_btn = table.find_element(By.TAG_NAME, "button")
    print(apply_btn.text)
    apply_btn.click()

    time.sleep(5)

    download_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a/span',
            )
        )
    )

    download_link.click()

    time.sleep(5)
    driver.close()


def __main__():
    # # url of the page we want to scrape
    url = "https://finance.yahoo.com/most-active"

    download_path = r"D:\USA\Artificial Stock market\backend\src\\"

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    # Finding the most-active table
    table = driver.find_element(By.TAG_NAME, "table")

    # each row has one a tag which is first column which can help
    # us to go at company page to access the historical data.
    # links = table.find_elements(By.TAG_NAME, "a")
    # companies = []
    tbody = driver.find_element(By.TAG_NAME, "tbody")
    # rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in tbody.find_elements(By.TAG_NAME, "tr"):
        columns = row.find_elements(By.TAG_NAME, "td")
        # print(columns)
        if columns != []:
            company = {
                "companyLogo": columns[0].text.strip(),
                "companyName": columns[1].text,
                "price": columns[2].text,
                "volume": columns[5].text,
                "marketCap": columns[7].text,
                "peRatio": columns[8].text,
            }
            print(company)
            print(columns[0].find_element(By.TAG_NAME, "a").get_attribute("href"))
            # history = get_history(
            #     columns[0].find_element(By.TAG_NAME, "a").get_attribute("href"), driver
            # )
            download_csv(
                columns[0].find_element(By.TAG_NAME, "a").get_attribute("href"), webdriver.Chrome(options = options)
            )
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            final_dir = os.path.join(cur_dir, 'src', ''+ company['companyLogo'] + ".csv")
            print(final_dir)
            history = get_history_from_csv(final_dir)
            company["data"] = history

            send_data_mongo(company)

            
            

    # for link in links:
    #     pass

    driver.close()


__main__()
