import datetime
import time
import DataAnalyse as da
import DataPreprocessor as dp
import TradeStrategy as ts
import Caching as cache
from KrakenAccount import KrakenAccount as KA
import threading

from Simulation import Simulation as sm


def print_asset_balance(account):
    balance = account.get_account_balance()

    for asset in balance:
        print('{:<6}:{:>10.5f}'.format(asset, float(balance[asset])))


def print_cash_balance(account, currency):
    cash = float(account.get_trade_balance(currency)['eb'])
    print('balance:', cash)


def get_last_ohlc(account, pair, int_min):
    result = {}
    prices = {}
    
    stop_timer = int(time.time() + (int_min * 60))

    while int(time.time()) != stop_timer:
        prices.setdefault(int(time.time()), account.get_ticker_info(pair)[pair]['c'][0])

    result['unixtime'] = list(prices.keys())[0]
    result['open'] = list(prices.values())[0]
    result['high'] = max(prices.values())
    result['low'] = min(prices.values())
    result['close'] = list(prices.values())[-1]
    
    return result


def sma(ohlcs, period=10, price='close'):
    _sum = 0.0
    
    if len(ohlcs) < period:
        return -1
    
    start = len(ohlcs) - period
    for ind in range(start, len(ohlcs)):
        _sum += float(ohlcs[ind][price])

    return _sum / period


def main():
    start_time = time.time()

    account = KA()
    pair = 'ETHUSDT'
    interval = 5
    period = 15
    ohlcs = []
    
    while time.localtime(time.time()).tm_sec != 0:
        pass

    start = time.ctime()

    while True:

        ohlc = get_last_ohlc(account, pair, interval) 
        ohlcs.append(ohlc) 
        print(ohlcs)
            
        SMA = sma(ohlcs, period, 'close')

        if SMA != -1:
            run_time = time.ctime()
            print(run_time, ' ', 'SMA_', period, ' = ', SMA, sep='')
     
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
'''
   pair = 'ETHUSDT'
    
    account = sm(100000)
    
    budget = account.get_budget()
    print('Primary budget', budget)

    previous_time = 0
    prev_slow_sma = 0
    prev_fast_sma = 0
    signal = 0
    interval = 5
    sleep = interval * 60 - 20
    while True:
        # The method gets PAIR and INTERVAL
        ohlc = dp.get_ohlc('ETHUSDT', interval)

        #cache.creation_or_updation_table_file('ETH_price.csv', ohlc, ['time', 'open', 'high', 'low', 'close'])
    
        if ohlc['time'].values[-1] != previous_time:
            curr_slow_sma = ts.SMA(ohlc, 'close', 120)
            curr_fast_sma = ts.SMA(ohlc, 'close', 60)

            print(dp.convert_unixtime(ohlc['time'].values[-1]), curr_slow_sma, curr_fast_sma)

            if prev_slow_sma != 0 and prev_fast_sma != 0:
                signal = ts.comparison_ma(prev_slow_sma, curr_slow_sma, prev_fast_sma, curr_fast_sma)

            if signal == -1 or signal == 1:
                print('Previous SMA', prev_slow_sma, prev_fast_sma)
                print('Current SMA', curr_slow_sma, curr_fast_sma)
                sgnl = [dp.convert_unixtime(ohlc['time'].values[-1]), ohlc['open'].values[-1], ohlc['high'].values[-1], ohlc['low'].values[-1], ohlc['close'].values[-1]]
                print(sgnl, 'BUY' if signal == 1 else 'SELL')

                #order = ts.creation_of_order(budget, 5, signal, pair)
                #account.add_position(order)
                #cache.creation_or_updation_table_file('Orders.csv', order.get_position(), ['id', 'Pair', 'Price', 'Volume', 'Type', 'Ordertype', 'Time', 'Position_cost'])
                #order.info_order()
                print()

            prev_ssma = curr_slow_sma
            prev_fsma = curr_fast_sma
            #cache.creation_or_updation_table_file('ETH_SMA.csv', [[curr_slow_sma, curr_fast_sma]], ['SMA_120', 'SMA_60'])

        previous_time = ohlc['time'].values[-1]
        time.sleep(sleep)
'''


