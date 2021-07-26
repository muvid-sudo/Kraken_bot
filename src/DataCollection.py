"""
The module is an implementation of data collection.
"""
import requests
import json
import time
import API as api


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
    position = api.kraken_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})
    position = json.loads(position.content)
    return position


def get_current_balance(currency):
    balance = api.kraken_request('/0/private/TradeBalance', {"nonce": str(int(1000 * time.time())), "asset": currency})
    balance = json.loads(balance.content)
    return balance
