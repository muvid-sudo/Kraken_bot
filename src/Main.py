import time
import DataCollection as dc
import DataOutput as do
from time import ctime
from email import utils
import datetime as dt
import pandas as pd
import os


def add_data_to_file(path, current_price):
    df = pd.read_csv(path, 'a+', header=1, names=['time', 'open', 'high', 'low', 'close'])
    print(df.head)
    last_time = df.at[df.index[-1],'time']
    print(last_time, current_price[0])
    #if int(last_time) < int(current_price[0]):
    #    df.append(current_price)
    #    df.to_csv(path, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)


if __name__ == '__main__':
    start_time = time.time()

    path_to_file = '../Data/price.csv'
    if not os.path.isfile(path_to_file):
        prices = open(path_to_file, 'w+')

    while True:
        price = dc.pair_price('ETHUSDT')

        current_price = [
                price[-1][0],
                price[-1][1],
                price[-1][2],
                price[-1][3],
                price[-1][4]
                ]

        if os.path.exists(path_to_file) and os.stat(path_to_file).st_size != 0:
            add_data_to_file(path_to_file, current_price)
        else:
            df = pd.DataFrame(price, columns=['time', 'open', 'high', 'low', 'close', '6', '7', '8'])
            df = df.drop(columns=['6', '7', '8'])
            df.to_csv(path_to_file, encoding='utf-8', index=False, columns=['time', 'open', 'high', 'low', 'close'], header=True)
        time.sleep(30)

    print("--- %s seconds ---" % (time.time() - start_time))
