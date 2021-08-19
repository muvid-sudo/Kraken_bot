import time
import DataCollection as dc
import DataAnalyse as da
import DataPreprocessor as dp
import TradeStrategy as ts
import Caching as cache


if __name__ == '__main__':
    start_time = time.time()

    previous_time = 0
    SF_SMA = []
    prev_ssma = 0
    prev_fsma = 0
    while True:
        ohlc = dp.get_ohlc('ETHUSDT', 1)

        cache.creation_or_updation_table_file('ETH_price.csv', ohlc, ['time', 'open', 'high', 'low', 'close'])
    
        if ohlc['time'].values[-1] != previous_time:
            SSMA = ts.SMA(ohlc, 'close', 120)
            FSMA = ts.SMA(ohlc, 'close', 60)
            ts.comparison_ma(prev_ssma, SSMA, prev_fsma, FSMA)
            prev_ssma = SSMA
            prev_fsma = FSMA
            SF_SMA.append([SSMA, FSMA])
            cache.creation_or_updation_table_file('ETH_SMA.csv', SF_SMA, ['SMA_120', 'SMA_60'])
        if len(SF_SMA) == 1000:
            SF_SMA.clear()
        previous_time = ohlc['time'].values[-1]
        time.sleep(30)

    print("--- %s seconds ---" % (time.time() - start_time))

   #cache.create_file('ETH_sma_60m.csv')
