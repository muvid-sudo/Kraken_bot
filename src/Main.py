import time
import DataCollection as dc
import DataOutput as do
from time import ctime
from email import utils
import datetime as dt
import pandas as pd
import os
import DataAnalyse as da

def add_data_to_file(path, updated_data):
    df = pd.read_csv(path)
    for row in updated_data:
        rows = [pd.Series(row, index=df.columns)]
        df = df.append(rows, ignore_index=True)
    df.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)


def create_file(filename):
    path = '../Data/%s' % filename
    if not os.path.isfile(path):
        price = open(path, 'w+')
    return path 


def edit_price_data(current_data):
    current_data = pd.DataFrame(current_data, columns=['time', 'open', 'high', 'low', 'close', '6', '7', '8'])
    current_data = current_data.drop(columns=['6', '7', '8'])
    return current_data


def get_new_data(curr_data, prev_data):
    curr_data = edit_price_data(curr_data)

    updated_data = []

    length_prev = len(prev_data)
    length_curr = len(curr_data)

    start = length_prev - length_curr

    for row in range(length_curr):
        if prev_data.values[start + row][0] != curr_data.values[row][0] and prev_data.values[start + row][0] < curr_data.values[row][0]:
            updated_data.append(curr_data.values[row])

    return updated_data


def collect_price_data(path, pair):
    #'ETHUSDT'
    current_data = dc.pair_price(pair)
    if os.path.exists(path) and os.stat(path).st_size != 0:
        previous_data = pd.read_csv(path)
        new_data = get_new_data(current_data, previous_data)
        add_data_to_file(path, new_data)
    else:
        current_data = edit_price_data(current_data)
        current_data.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)


if __name__ == '__main__':
    start_time = time.time()

    path = create_file('price.csv')
    
    previous_time = 0
    count = 1
    LEMA = 0.0 
    while True:
        collect_price_data(path, 'ETHUSDT')
        data = pd.read_csv(path)
        if count == 1:
            LEMA = da.CSMA(data, price='close', period=30)
            count -= 1
        if int(data['time'].values[-1]) != previous_time:
            SMA = da.CSMA(data, price='close', period=30)
            EMA = da.CEMA(data, LEMA, price='close', period=30)
            LEMA = EMA
            print('%.2f' % SMA, '%.2f' % EMA)
        previous_time = int(data['time'].values[-1])
        time.sleep(30)

    
    #FMA, SMA = da.moving_average(data, fast_period=5, slow_period=10)
    #MA_1 = da.SMA(data, period=5)
    #MA_2 = da.SMA(data, period=10)
    #EMA = da.EMA(data, period=5)

    #l_1 = len(FMA) if len(FMA) > len(SMA) else len(SMA)
    #l_2 = len(MA_1) if len(MA_1) > len(MA_2) else len(MA_2)
    #
    #boundary = l_1 if l_1 > l_2 else l_2 
    #print('FMA_1', 'FMA_2', 'SMA_1', 'SMA_2', 'EMA', sep='\t')
    #for value in range(boundary):
    #    try:
    #        print('%.2f' % FMA[value], '%.2f' % MA_1[value], '%.2f' % SMA[value], '%.2f' % MA_2[value], '%.2f' % EMA[value], sep='\t')
    #    except KeyError:
    #        continue
    #print(da.comparison_ma(FMA, SMA))

    # do.some_graph(data)
       #do.get_candle_graph(data)

    print("--- %s seconds ---" % (time.time() - start_time))
