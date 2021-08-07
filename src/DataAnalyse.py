import pandas as pd
import matplotlib.pyplot as plt


def moving_average(data, price_type='open', fast_period=30, slow_period=10):
    FMA = data[price_type].rolling(window=fast_period).mean() 
    SMA = data[price_type].rolling(window=slow_period).mean()
    return FMA, SMA


def comparison_ma(FMA, SMA):
    if FMA.values[-1] == SMA.values[-1] and FMA.values[-2] > SMA.values[-2]:
        return 'sell'
    elif FMA.values[-1] == SMA.values[-1] and FMA.values[-2] < SMA.values[-2]:
        return 'buy' 


def comparison_history_ma(FMA, SMA, data):
    print(len(FMA), len(SMA), len(data))


    length_fma = len(FMA)
    length_sma = len(SMA)

    main_length = length_fma if length_fma > length_sma else length_sma

    for value in range(main_length):
        if FMA[value] == SMA[value]:
            print('sell', data['open'].values[value])
        elif FMA[value] == SMA[value]: 
            print('buy', data['open'].values[value])
        

def get_moving_average(data, price='open', fast_period=10, slow_period=30):
    pass
