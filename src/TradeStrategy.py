import DataAnalyse as da
import DataPreprocessor as dp

from Simulation import Simulation as sm
from Position import Position as pos

def creation_of_order(budget, share_of_order, signal, pair):
    if share_of_order > 0 and share_of_order <= 100:
        share_of_order /= 100
    elif share_of_order < 0 and share_of_order > 100:
        share_of_order = 0.5

    amount_of_cash = budget * share_of_order 

    if signal == -1:
        type_ = 'sell'
    else:
        type_ = 'buy'

    price = float(dp.get_ask_price(pair))
    volume = amount_of_cash / price
    time = dp.get_current_server_time()
    time = dp.convert_unixtime(float(time))

    #print('pair: %s' % pair, 'price: %s' % price, 'volume: %s' % volume, 'type: %s' % type_, 'Amount: %s' % amount_of_cash, 'time: %s' % time, sep='\n')

    position = pos(pair, price, volume, type_, 'limit', time, amount_of_cash)
 
    return position


'''
    The method returns a signal about intersection SMAs:
-1: SELL
+1: BUY
0:  NOTHING
'''
def comparison_ma(prev_slow, curr_slow, prev_fast, curr_fast):
    if prev_fast > curr_fast and curr_fast < curr_slow:
        return -1
    elif prev_fast < curr_fast and curr_fast > curr_slow:
        return 1
    return 0
    

# The method builds a current moving average.
def SMA(data, price='open', period=10):
    SMA = 0.0

    num_of_rows = len(data)
    learned_start = num_of_rows - period

    sum_for_period = 0
    for val in data[price].values[learned_start:num_of_rows]:
        sum_for_period += float(val)
    SMA = sum_for_period / period 

    return SMA 


# The method builds a current exponential moving average
def CEMA(data, LEMA, price='open', period=10, smoothing=2):
    EMA = 0.0

    num_of_rows = len(data)
    smoothing_factor = smoothing / period + 1

    EMA = (data[price].values[-1] * smoothing_factor) + LEMA * (1 - smoothing_factor)

    return EMA
