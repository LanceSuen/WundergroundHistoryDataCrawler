# Author : lianlongsun@gmail.com

import time
import csv
import sys
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.proxy import Proxy, ProxyType


def requestAndSave(date,driver):

    url = 'https://www.wunderground.com/history/daily/cn/shanghai-hongqiao/ZSSS/date/' + date
    driver.get(url) 
    time.sleep(5)
    tablelist = driver.find_elements_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table')
    table = tablelist[0]
    with open(date[:-6]+'.csv', 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements_by_css_selector('tr')[1:]:
            temp = [d.text for d in row.find_elements_by_css_selector('td')]
            temp.append(date)
            print(temp)
            wr.writerow(temp)

def main():
    # Options 
    path_to_extension = r'./uBlock'
    path_to_webdriver = './chromedriver'
    chrome_options = webdriver.ChromeOptions()

    
    #chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1086")
    chrome_options.add_argument('load-extension=' + path_to_extension)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = Chrome(chrome_options=chrome_options)
    #driver = Chrome()
    y1 = int(sys.argv[1])
    y2 = int(sys.argv[2])

    d1 = date(y1, 1, 1)
    d2 = date(y2, 1, 1)
    delta = d2 - d1
    for i in range(delta.days + 1):
        print('Crawling ' + str(d1 + timedelta(days=i)))
        try:
            requestAndSave(str(d1 + timedelta(days=i)), driver)
        except:
            print('No DATA on ' + str(d1 + timedelta(days=i)))

main()