"""
The module is an implementation of data collection.
"""
import requests
import json

import API as api


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data):
    headers = {'API-Key': api.api_key, 'API-Sign': get_kraken_signature(uri_path, data, api.api_sec)}
    # get_kraken_signature() as defined in the 'Authentication' section
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
    price = 0
    try:
        price = data['result'][pair][-1][0]
        return price
    except KeyError:
        return 0
