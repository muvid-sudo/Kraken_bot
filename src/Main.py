import time
import DataCollection as dc
import DataAnalyse as da
import DataPreprocessor as dp
import TradeStrategy as ts
import Caching as cache


if __name__ == '__main__':
    start_time = time.time()

    previous_time = 0
    SSMA = []
    FSMA = []
    while True:
        ohlc = dp.get_ohlc('ETHUSDT', 1)

        cache.creation_or_updation_table_file('ETH1_price.csv', ohlc, ['time', 'open', 'high', 'low', 'close'])
    
        if ohlc['time'].values[-1] != previous_time:
            SSMA.append(ts.SMA(ohlc, 'close', 120))
            FSMA.append(ts.SMA(ohlc, 'close', 60))
            cache.creation_or_updation_table_file('ETH_sma_120m.csv', SSMA, ['SMA_120'])
        previous_time = ohlc['time'].values[-1]
        time.sleep(30)

    print("--- %s seconds ---" % (time.time() - start_time))

   #cache.create_file('ETH_sma_60m.csv')
