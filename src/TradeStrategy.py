import DataAnalyse as da
import DataPreprocessor as dp


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
