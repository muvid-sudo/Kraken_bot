import pandas as pd
import matplotlib.pyplot as plt
import DataCollection as dc
import DataPreprocessor as dp


def get_list_unique_items(table, column):
    pairs = []

    for val in table:
        if pairs.count(val[column]) == 0:
            pairs.append(val[column])

    return pairs

    
def historical_price(path, pair):
    #'ETHUSDT'
    data = dc.get_ohlc(pair)
    if os.path.exists(path) and os.stat(path).st_size != 0:
        previous_data = pd.read_csv(path)
        new_data = get_new_data(current_data, previous_data)
        add_data_to_file(path, new_data)
    else:
        current_data = edit_price_data(current_data)
        current_data.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)


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
    
    num_of_rows = len(data[price].values)

    for ind in range(num_of_rows):
        
        if ind + period >= num_of_rows - period:
            break
        average_val_for_period = sum(data[price].values[ind:count+period]) / period

        SMA.append(average_val_for_period)

    return SMA


# The method builds historical exponential moving average
def HEMA(data, price='open', period=10, smoothing_factor=2):
    SMA = 0.0
    num_of_rows = len(data[price].values)
    SMA = sum(data[price].values[0:period]) / period
            
    EMA = [0 for i in range(period - 1)]
    EMA.append(SMA)

    smoothing = smoothing_factor / period + 1
    num_of_rows = len(data[price].values)

    for ind in range(period, num_of_rows):
        EMA.append((data[price].values[ind] * smoothing) + EMA[ind - 1] * (1 - smoothing))

    return EMA


