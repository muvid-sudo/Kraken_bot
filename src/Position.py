'''
resp = kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "limit",
    "type": "buy",
    "volume": 1.25,
    "pair": "XBTUSD",
    "price": 27500
}, api_key, api_sec)

'''
from itertools import count


class Position:
    id_order = count(0) 
    ordertype = 'limit'
    type_ = ''
    volume = 0.0
    pair = ''
    price = 0.0
    unixtime = 0.0
    position_cost = 0.0
    position = []


    def __init__(self, pair, price, volume, type_, ordertype, unixtime, position_cost):
        self.id = next(self.id_order)
        self.pair = pair
        self.price = price
        self.volume = volume
        self.type_ = type_
        self.ordertype = ordertype
        self.unixtime = unixtime
        self.position_cost = position_cost
        self.position.append([self.id, self.pair, self.price, self.volume, self.type_, self.ordertype, self.unixtime, self.position_cost])


    def info_order(self):
        print('ID: %s' % self.id, 'Pair: %s' % self.pair, 'Price: %s' % self.price, 'Volume: %s' % self.volume, 'Type: %s' % self.type_, 'Ordertype: %s' % self.ordertype, 'Time: %s' % self.unixtime, 'Position_cost: %s' % self.position_cost, sep='\n')

    
    def get_position_cost(self):
        return self.position_cost
    

    def get_position(self):
        return self.position
