import time
import DataCollection as dc
import DataOutput as do
from time import ctime
from email import utils
import datetime as dt
import pandas as pd
import os


def add_data_to_file(path, updated_data):
    df = pd.read_csv(path)
    last_time = df.at[df.index[-1],'time']
    for row in updated_data: 
        rows = [pd.Series(row, index=df.columns)]
        df = df.append(rows, ignore_index=True)
    df.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)


def create_file(filename):
    path = '../Data/%s' % filename
    if not os.path.isfile(path):
        prices = open(path, 'w+')
    return path 


def get_new_data(curr_data, prev_data):
    curr_data = pd.DataFrame(curr_data, columns=['time', 'open', 'high', 'low', 'close', '6', '7', '8'])
    curr_data = curr_data.drop(columns=['6', '7', '8'])

    updated_data = []

    length_prev = len(prev_data)
    length_curr = len(curr_data)

    start = length_prev - length_curr

    for row in range(length_curr):
        if prev_data.values[start + row][0] != curr_data.values[row][0] and prev_data.values[start + row][0] < curr_data.values[row][0]:
            updated_data.append(curr_data.values[row])

    return updated_data


if __name__ == '__main__':
    start_time = time.time()

    path = create_file('price.csv')    

    while True:
        current_data = dc.pair_price('ETHUSDT')
        
        if os.path.exists(path) and os.stat(path).st_size != 0:
            previous_data = pd.read_csv(path)
            new_data = get_new_data(current_data, previous_data)
            add_data_to_file(path, new_data)
        else:
            current_data.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)
        time.sleep(30)

    print("--- %s seconds ---" % (time.time() - start_time))
