import configparser
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time


QUERY = {
# MARKET DATA
    'get_server_time' : '/0/public/Time',
    'get_system_status' : '/0/public/SystemStatus',
    'get_asset_info' : '/0/public/Assets',
    'get_tradable_info' : '/0/public/AssetPairs',
    'get_ticker_info' : '/0/public/Ticker',
    'get_ohlc_info' : '/0/public/OHLC',
    'get_order_book' : '/0/public/Depth', 
    'get_recent_trades' : '/0/public/Trades',
    'get_recent_spreads' : '/0/public/Spread',

# USER DATA
    'get_account_balance' : '/0/private/Balance',
    'get_trade_balance' : '/0/private/TradeBalance',
    'get_open_orders' : '/0/private/OpenOrders',
    'get_closed_orders' : '/0/private/ClosedOrders',
    'get_orders_info' : '/0/private/QueryOrders',
    'get_trades_history' : '/0/private/TradesHistory',
    'get_trades_info' : '/0/private/QueryTrades',
    'get_open_positions' : '/0/private/OpenPositions',
    'get_ledgers_info' : '/0/private/Ledgers',
    'get_ledgers' : '/0/private/QueryLedgers',
    'get_trade_volume' : '/0/private/TradeVolume',

# USER TRADING
    'add_order' : '/0/private/AddOrder',
    'cancel_order' : '/0/private/CancelOrder',
    'cancel_all_orders' : '/0/private/CancelAll',
    'cancel_all_orders_after_x' : '/0/private/CancelAllOrdersAfter',
}


class KrakenAccount:


    def __init__(self):
       
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.URL = config['KRAKEN_API']['api_url']
        self.PbK = config['KRAKEN_API']['api_key']
        self.PrK = config['KRAKEN_API']['api_sec']


    def _get_kraken_signature(urlpath, data, secret):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()


    # Attaches auth headers and returns results of a POST request
    def _kraken_request(self, method_name, params=None, data=None):
        url_path = QUERY[method_name]

        if data == None:
            data = {
                    'nonce' : str(int(1000 * time.time()))
            }
        else:
            data['nonce'] = str(int(1000 * time.time())) 

        headers = {
                'API-Key': self.PbK, 
                'API-Sign': KrakenAccount._get_kraken_signature(url_path, data, self.PrK)
        }

        # get_kraken_signature() as defined in the 'Authentication' section
        url = self.URL + url_path

        if url_path.count('private'):
            req = requests.post(url, headers=headers, data=data)
        else:
            req = requests.get(url, params=params)
        
        response = req.json()['result']

        return response


    ''' MARKET DATA '''

    def get_server_time(self):
        method_name = self.get_server_time.__name__
        response = self._kraken_request(method_name)
        return response 

    def get_system_status(self):
        method_name = self.get_system+_status.__name__
        response = self._kraken_request(method_name)
        return response 


    def get_asset_info(self):
        method_name = self.get_asset_info.__name__
        response = self._kraken_request(method_name)
        return response 


    def get_tradable_info(self, pair):
        method_name = self.get_tradable_info.__name__
        params = {
                'pair' : pair
        }
        response = self._kraken_request(method_name, params=params)
        return response 


    def get_ticker_info(self, pair):
        method_name = self.get_ticker_info.__name__
        params = {
                'pair' : pair
        }
        response = self._kraken_request(method_name, params=params)
        return response 


    def get_ohlc_info(self, pair, interval, since):
        method_name = self.get_ohlc_info.__name__
        params = {
                'pair' : pair,
                'interval' : interval,
                'since' : since
        }
        response = self._kraken_request(method_name, params=params)
        return response 

    
    def get_order_book(self, pair, count=100):
        method_name = self.get_order_book.__name__
        params = {
                'pair' : pair,
                'count' : count
        }
        response = self._kraken_request(method_name, params=params)
        return response 


    def get_recent_trades(self, pair, since):
        method_name = self.get_recent_trades.__name__
        params = {
                'pair' : pair,
                'since' : since
        }
        response = self._kraken_request(method_name, params=params)
        return response


    def get_recent_spreads(self, pair, since):
        method_name = self.get_recent_spreads.__name__
        params = {
                'pair' : pair,
                'since' : since
        }
        response = self._kraken_request(method_name, params=params)
        return response
    

    ''' USER DATA '''

    def get_account_balance(self):
        method_name = self.get_account_balance.__name__
        response = self._kraken_request(method_name)
        return response


    def get_trade_balance(self, asset):
        method_name = self.get_trade_balance.__name__
        data = {
                'asset' : asset
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_open_orders(self, trades=True):
        method_name = self.get_open_orders.__name__
        data = {
                'trades' : trades
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_closed_orders(self, trades=False, start=0, end=0, closetime='both'):
        method_name = self.get_closed_orders.__name__
        data = {
                'trades' : trades,
                'start' : start,
                'end' : end,
                'closetime' : closetime
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_orders_info(self, trades, txid):
        method_name = self.get_orders_info.__name__ 
        data = {
                'trades' : trades,
                'txid' : txid
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_trades_history(self, _type='all', trades=False, start=0, end=0):
        method_name = self.get_trades_history.__name__
        data = {
                'type' : _type,
                'trades' : trades,
                'start' : start,
                'end' : end
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_trades_info(self, txid, trades=False):
        method_name = self.get_trades_info.__name__
        data = {
                'txid' : txid,
                'trades' : trades
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_open_positions(self, txid=None, docalcs=False, consolidation='market'):
        method_name = self.get_open_positions.__name__
        data = {
                'docalcs' : docalcs,
                'consolidation' : consolidation
        }
        if txid != None: 
            data['txid'] = txid
        response = self._kraken_request(method_name, data=data)
        return response


    def get_ledgers_info(self, asset='all', aclass='currence', _type='all', start=0, end=0):
        method_name = self.get_ledgers_info.__name__
        data = {
                'asset' : asset,
                'aclass' : aclass,
                'type' : _type,
                'start' : start,
                'end' : end
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def get_ledgers(self, _id=None, trades=False):
        method_name = self.get_ledgers.__name__
        data = {
                'trades' : trades
        }
        if _id != None:
            data['id'] = _id
        response = self._kraken_request(method_name, data=data)
        return response


    def get_trade_volume(self, pair, fee_info=True):
        method_name = self.get_trade_volume.__name__
        data = {
                'pair' : pair,
                'fee_info' : fee_info
        }
        response = self._kraken_request(method_name, data=data)
        return response


    ''' USER DATA '''

    def add_order(self, 
            ordertype, _type, volume, pair, price, 
            price2=None, leverage=None, oflags=None, 
            timeinforce='GTC', 
            starttm=0, expiretm=0, 
            close=None):
        method_name = self.add_order.__name__
        data = {
                'ordertype' : ordertype,
                'type' : _type,
                'pair' : pair,
                'volume' : volume,
                'price' : price
        }
        response = self._kraken_request(method_name, data=data)
        return response


    def cancel_order(self):
        pass


    def cancel_all_orders(self):
        pass


    def cancel_all_orders_after_x(self):
        pass

