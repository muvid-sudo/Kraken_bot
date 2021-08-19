"""
The module is an implementation of data collection.
"""
import requests
import json
import time
import datetime
from forex_python.converter import CurrencyRates
import API as api



'''
    The method returns Asset ticker Info:
    The list has several keys:
a: Ask [<price>, <whole lot volume>, <lot volume>]
b: Bid [<price>, <whole lot volume>, <lot volume>]
c: Last trade closed [<price>, <lot volume>]
v: Volume [<today>, <last 24 hours>]
p: Volume weighted average price [<today>, <last 24 hours>]
t: Number of trades [<today>, <last 24 hours>]
l: Low [<today>, <last 24 hours>]
h: High [<today>, <last 24 hours>]
o: Today's opening price
'''
def get_current_ticker_info(pair):
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=%s' % pair)
    return resp.json()['result'][pair]


'''
    The method returns OHLC ticker information:
    The list has several keys:
int     <time> 
string  <open> 
string  <high> 
string  <low> 
string  <close> 
string  <vwap>
string  <volume> 
int     <count>
'''
def get_pair_price(pair, interval):
    resp = requests.get('https://api.kraken.com/0/public/OHLC?pair=%s&interval=%d' % (pair, interval))
    return resp.json()['result'][pair]


'''
    The method returns server's time
    The list has several keys:
unixtime
rfc1123
'''
def get_server_time():
    time = requests.get('https://api.kraken.com/0/public/Time')
    return time.json()['result'] 


'''
    The method returns an information about balance:
    The list contains the following keys:
eb: Equivalent balance (combined balance of all currencies)
tb: Trade balance (combined balance of all equity currencies)
m: Margin amount of open positions
n: Unrealized net profit/loss of open positions
c: Cost basis of open positions
v: Current floating valuation of open positions
e: Equity: trade balance + unrealized net profit/loss
mf: Free margin: Equity - initial margin (maximum margin available to open new positions)
ml: Margin level: (equity / initial margin) * 100
'''
def get_trade_balance(currency):
    resp = api.kraken_request('/0/private/TradeBalance', {"nonce": str(int(1000*time.time())), "asset": currency})
    return resp.json()['result']


'''
    The method returns current open positions and their amount:
    The list contains one key:
Asset : Amount
'''
def get_account_balance():
    position = api.kraken_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})
    return position.json()['result']

'''
    The method returns an exchange rate of specified pair
'''
def exchange_rate(source_currency='USD', target_currency='RUB'):
    c = CurrencyRates()
    return c.get_rate(source_currency, target_currency)

'''
    THe method returns 
'''
def get_current_price(pair):
    tickers = 'https://api.kraken.com/0/public/Trades?pair=%s'
    data = json.loads(requests.get(tickers % pair).content)
    return data['result']


'''
    The method returns historical orders:
    The list contains the following key:
ordertxid   Order responsible for execution of trade
pair        Asset pair
time        Unix timestamp of trade
type        Type of order (buy/sell)
ordertype   Order type
price       Average price order was executed at (quote currency)
cost        Total cost of order (quote currency)
fee         Total fee (quote currency)
vol         Volume (base currency)
margin      Initial margin (quote currency)
misc        Comma delimited list of miscellaneous info:
'''
def get_historical_orders():
    previous_orders = api.kraken_request('/0/private/TradesHistory', {"nonce": str(int(1000*time.time())), "trades": True})
    return previous_orders.json()['result']['trades']

