import DataAnalyse as da
import DataPreprocessing as dp





def comparison_ma(FMA, SMA):
    if FMA.values[-1] == SMA.values[-1] and FMA.values[-2] > SMA.values[-2]:
        return 'sell'
    elif FMA.values[-1] == SMA.values[-1] and FMA.values[-2] < SMA.values[-2]:
        return 'buy' 


def analyze_current_moving_average(pair, price='close', fast_period=10, slow_period=30):
    ohlc = get_ohlc(pair)
    fma = da.SMA(ohlc, price, fast_period)
    sma = da.SMA(ohlc, price, slow_period)



