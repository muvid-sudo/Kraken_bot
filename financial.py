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
    

def getGraph(prices):
    plt.xlabel('Time', fontsize=10)
    plt.ylabel('Price', fontsize=10)
    plt.plot(prices.keys(), sorted(prices.values()))
    plt.show()
    
    
def getCurrPrice(pair):
    tickers = 'https://api.kraken.com/0/public/Trades?pair=%s'
    data = json.loads(requests.get(tickers % pair).content)
    price = data['result'][pair][-1][0]
    return price
    
    
def getPriceForPeriod(pair, period):
    prices = {}
    curr = 0
    prev = 0
    t_end = time.time() + 60 * period
    while (time.time() < t_end):
        curr = getCurrPrice(pair)
        
        timestamp = findTime(time.asctime(time.localtime(time.time())))
        prices[timestamp] = curr 
        
        time.sleep(1)
            
    return prices 


def main():
    # dictionary, key(time) -> value(price)
    prices = {}
    # pair, period
    prices = getPriceForPeriod('ETHUSDT', 60)
    getGraph(prices)
    print("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
