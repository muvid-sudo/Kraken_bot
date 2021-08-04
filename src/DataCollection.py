"""
The module is an implementation of data collection.
"""
import requests
import json
import time
import API as api
import DataOutput as do
from tradingview_ta import *


def ask_bid_info(pair):
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=%s' % pair)
    return resp.json()['result'][pair]


def pair_price(pair):
    resp = requests.get('https://api.kraken.com/0/public/OHLC?pair=%s' % pair)
    return resp.json()['result'][pair]


def get_ticker():
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=TBTCUSD')
    print(resp.json()['result']['TBTCUSD'])


def get_server_time():
    resp = requests.get('https://api.kraken.com/0/public/Time')
    print(resp.json())


def some():
    tesla = TA_Handler(
        symbol="TSLA",
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_1_DAY
    )
    print(tesla.get_analysis().summary)
    analysis = get_multiple_analysis(screener="america", interval=Interval.INTERVAL_1_HOUR,
                                     symbols=["nasdaq:tsla", "nyse:docn", "nasdaq:aapl"])
    print(analysis)


def get_pair_price(pair):
    tickers = 'https://api.kraken.com/0/public/Trades?pair=%s'
    data = json.loads(requests.get(tickers % pair).content)
    # Sometimes there is an error that is an absence of key 'result'
    try:
        return data['result'][pair]
    except KeyError:
        return -1


def get_current_price(pair):
    tickers = 'https://api.kraken.com/0/public/Trades?pair=%s'
    data = json.loads(requests.get(tickers % pair).content)
    # Sometimes there is an error that is an absence of key 'result'
    try:
        return data['result'][pair][-1][0]
    except KeyError:
        return -1


def get_current_balance(currency):
    balance = api.kraken_request('/0/private/TradeBalance', {"nonce": str(int(1000 * time.time())), "asset": currency})
    balance = json.loads(balance.content)
    return balance


def get_open_positions():
    position = api.kraken_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})
    position = json.loads(position.content)
    return position


def get_open_orders():
    open_orders = api.kraken_request('/0/private/OpenOrders', {"nonce": str(int(1000 * time.time())), "trades": True})
    open_orders = json.loads(open_orders.content)
    return open_orders


def get_closed_orders():
    closed_orders = api.kraken_request('/0/private/ClosedOrders', {"nonce": str(int(1000 * time.time())), "userref": 36493663})
    closed_orders = json.loads(closed_orders.content)
    return closed_orders


def get_previous_orders():
    previous_orders = api.kraken_request('/0/private/TradesHistory', {"nonce": str(int(1000*time.time())), "trades": True})
    previous_orders = json.loads(previous_orders.content)
    return previous_orders


def get_information_order(order_id):
    order_info = api.kraken_request('/0/private/QueryTrades', {"nonce": str(int(1000*time.time())), "txid": order_id, "trades": True})
    order_info = json.loads(order_info.content)
    return order_info


def get_open_margin_positions():
    order_info = api.kraken_request('/0/private/OpenPositions', {"nonce": str(int(1000*time.time())), "docalcs": True})
    order_info = json.loads(order_info.content)
    return order_info


def amount_previous_orders(numbers):
    trades = get_previous_orders()
    orders_tid = []

    for order in trades['result']['trades']:
        orders_tid.append(order)
        numbers -= 1
        if numbers == 0:
            break

    result = []
    for tid in orders_tid:
        result.append(trades['result']['trades'][tid])

    return result


def get_price_period(pair, period):
    timestamps = []
    prices = []
    t_end = time.time() + 60 * period
    previous_price = 0
    while time.time() < t_end:
        current_price = float(get_current_price(pair))
        timestamp = do.find_time(time.asctime(time.localtime(time.time())))
        if current_price != previous_price and current_price > 0:
            timestamps.append(timestamp)
            prices.append(current_price)
        previous_price = current_price
    time_and_price = {'Time': timestamps, 'Price': prices}
    return time_and_price
