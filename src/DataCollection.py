"""
The module is an implementation of data collection.
"""
import requests
import json
import time
import API as api


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data):
    headers = {}
    headers['API-Key'] = api.api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = api.get_kraken_signature(uri_path, data, api.api_sec)
    req = requests.post((api.api_url + uri_path), headers=headers, data=data)
    return req


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_current_price(pair):
    tickers = 'https://api.kraken.com/0/public/Trades?pair=%s'
    data = json.loads(requests.get(tickers % pair).content)
    # Sometimes there is an error that is an absence of key 'result'
    try:
        price = data['result'][pair][-1][0]
        return price
    except KeyError:
        return -1


def get_current_positions():
    position = kraken_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})
    position = json.loads(position.content)
    return position


def get_current_balance(currency):
    balance = kraken_request('/0/private/TradeBalance', {"nonce": str(int(1000 * time.time())), "asset": currency})
    balance = json.loads(balance.content)
    return balance
