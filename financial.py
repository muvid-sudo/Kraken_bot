import time
import os
import requests
import json
import time
import pykrakenapi as k
from decimal import Decimal
from email import utils
import matplotlib.pyplot as plt

start_time = time.time()

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = ''
api_sec = ''

# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

    
def findTime(time):
    date = utils.parsedate_to_datetime(time)
    #date.strftime('%d/%b/%Y')
    return date.strftime('%H:%M')
    

def getGraph(price, curr_time):
    plt.xlabel('Price', fontsize=10)
    plt.ylabel('Time', fontsize=10)  
    plt.plot(curr_time, price)
    plt.show()
    
    
def getCurrPrice(pair):
    tickers = 'https://api.kraken.com/0/public/Trades?pair=%s'
    data = json.loads(requests.get(tickers % pair).content)
    price = data['result'][pair][-1][0]
    return price
    
    
def getPriceForPeriod(pair, freqUpdate, period):
    prices = []
    price_time = []
    curr = 0
    prev = 0
    tic = 0
    while (tic != period):
        curr = getCurrPrice(pair)
        
        if curr != prev:
            prices.append(curr)
            price_time.append(findTime(time.asctime(time.localtime(time.time()))))
        
        prev = curr 
        
        time.sleep(freqUpdate)
        tic += 1
    
    return prices, price_time 


if __name__ == '__main__':
    prices = []
    times = []
    prices, times = getPriceForPeriod('ETHUSDT', 2, 100)
    print(prices)
    getGraph(prices, times)
    print("--- %s seconds ---" % (time.time() - start_time))
