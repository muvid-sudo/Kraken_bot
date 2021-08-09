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
        

# The method builds historical simple moving average
def HSMA(data, price='open', period=10):
    SMA = [0 for i in range(period - 1)]
    
    average_val = 0
    num_of_rows = len(data[price].values)

    for ind in range(num_of_rows):
        price_sum  = 0
        

        for count in range(period):
            if ind + count >= num_of_rows:
                #average_val = price_sum / period
                #SMA.append(average_val)
                break
            price_sum += data[price].values[ind + count] 

        average_val = price_sum / period
        SMA.append(average_val)

    return SMA


# The method builds historical expotential moving average
def HEMA(data, price='open', period=10, smoothing_factor=2):
    sum_value = 0.0
    SMA = 0.0
    num_of_rows = len(data[price].values)
    
    for ind in range(period):
        sum_value += data[price].values[ind]
        SMA = sum_value / period
            
    EMA = [0 for i in range(period - 1)]
    EMA.append(SMA)

    smoothing = smoothing_factor / period + 1
    
    average_val = 0
    num_of_rows = len(data[price].values)

    for ind in range(period, num_of_rows):
        EMA.append((data[price].values[ind] * smoothing) + EMA[ind - 1] * (1 - smoothing))

    return EMA


# The method builds a current moving average.
def CSMA(data, price='open', period=10):
    SMA = 0.0

    num_of_rows = len(data)
    learned_start = num_of_rows - period

    prices_sum = 0.0
    for val in range(learned_start, num_of_rows):
        prices_sum += data[price].values[val]

    SMA = prices_sum / period

    return SMA 


def CEMA(data, LEMA, price='open', period=10, smoothing=2):
    EMA = 0.0

    num_of_rows = len(data)
    learned_start = num_of_rows - period

    smoothing_factor = smoothing / period + 1

    EMA = (data[price].values[-1] * smoothing_factor) + LEMA * (1 - smoothing_factor)

    return EMA
'''
period = 5

0   1   2   3   4   5   6   7   8   9
1   2   3   4   5   6   7   8   9   10

head = 0

start_ind = 0
end_ind = 4

current_sum = 1 + 2 + 3 + 4 + 5
average_sum = 10 / period

last_sum = price_sum # 10
head = 4

start_ind = 5
end_ind = 9

price_sum = 6 + 7 + 8 + 9 + 10 



'''
