import time
import DataCollection as dc
import DataAnalyse as da
import DataPreprocessor as dp
import TradeStrategy as ts
import Caching as cache

from Simulation import Simulation as sm

if __name__ == '__main__':
    start_time = time.time()

    pair = 'ETHUSDT'
    
    account = sm(100000)
    
    budget = account.get_budget()
    print('Primary budget', budget)

    previous_time = 0
    prev_slow_sma = 0
    prev_fast_sma = 0
    while True:
        # The method gets PAIR and INTERVAL
        ohlc = dp.get_ohlc('ETHUSDT', 1)

        #cache.creation_or_updation_table_file('ETH_price.csv', ohlc, ['time', 'open', 'high', 'low', 'close'])
    
        if ohlc['time'].values[-1] != previous_time:
            curr_slow_sma = ts.SMA(ohlc, 'close', 120)
            curr_fast_sma = ts.SMA(ohlc, 'close', 60)

            signal = ts.comparison_ma(prev_slow_sma, curr_slow_sma, prev_fast_sma, curr_fast_sma)

            if signal == -1 or signal == 1:
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
        time.sleep(30)

    print("--- %s seconds ---" % (time.time() - start_time))

   #cache.create_file('ETH_sma_60m.csv')
