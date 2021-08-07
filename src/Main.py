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
        edit_price_data(current_data)
        current_data.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)


if __name__ == '__main__':
    start_time = time.time()

    path = create_file('price.csv')

    while True:
        collect_price_data(path, 'ETHUSDT')
        data = pd.read_csv(path)
        FMA, SMA = da.moving_average(data, fast_period=5, slow_period=10)
        print(da.comparison_ma(FMA, SMA))
        time.sleep(30)

    # do.some_graph(data)
       #do.get_candle_graph(data)

    print("--- %s seconds ---" % (time.time() - start_time))
