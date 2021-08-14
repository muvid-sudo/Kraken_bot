import pandas as pd
import DataCollection as dc


'''
    The method returns current server's time
returns: date time
'''
def get_current_server_time():
    unix_time = dc.get_server_time()['unixtime']
    return datetime.datetime.fromtimestamp(int(unix_time))


def get_equivalent_balance(currency):
    balance = dc.get_trade_balance(currency)['eb']
    return balance


'''
    The method returns the last closed trade price.
'''
def get_last_closed_trade(pair):
    closed_trade_price = dc.get_current_ticker_info(pair)['c'][0]
    return closed_trade_price


'''
    The method returns an ask price.
'''
def get_ask_price(pair):
    ask_price = dc.get_current_ticker_info(pair)['a'][0]
    return ask_price


'''
    The method returns an ask price.
'''
def get_bid_price(pair):
    bid_price = dc.get_current_ticker_info(pair)['b'][0]
    return bid_price


'''
    The method returns OHLC ticker information:
    The list contains the following columns:
string - time - seconds
string - open 
string - high
string - low
string - close
'''
def get_ohlc(pair, interval):
    ohlc = dc.get_pair_price(pair, interval)
    ohlc = pd.DataFrame(ohlc, columns=['time', 'open', 'high', 'low', 'close', '6', '7', '8'])
    ohlc = ohlc.drop(columns=['6', '7', '8'])
    return ohlc 


'''
    The method returns a list open positions
'''
def get_open_positions():
    positions = dc.get_account_balance()
    result = []
    for i in positions:
        result.append([i, positions[i]])
    return result


'''
    The method returns current pair price
'''
def get_current_pair_price(pair):
    data = dc.get_current_price(pair)
    return float(data[pair][-1][0])


def get_historical_orders():
    data = dc.get_historical_orders()
    
    orders = []
    headers = ['ordertxid', 'postxid', 'pair', 'time', 'type', 'ordertype', 'price', 'cost', 'fee', 'vol', 'margin', 'misc']
    for i in data:
        orders.append( 
                [ data[i][headers[0]], data[i][headers[1]], data[i][headers[2]], data[i][headers[3]], data[i][headers[4]], data[i][headers[5]], data[i][headers[6]], 
                    data[i][headers[7]], data[i][headers[8]], data[i][headers[9]], data[i][headers[10]], data[i][headers[11]] ]
                )

    return orders 
