import matplotlib.pyplot as plt
from time import ctime
from email import utils
import pandas as pd
import shrimpy
import plotly.graph_objects as go
import DataPreprocessor as dp
import datetime

def print_orders(table):
    table.sort(key=lambda row: row[3])
    headers = ['ordertxid', 'postxid', 'pair', 'time', 'type', 'ordertype', 'price', 'cost', 'fee', 'vol', 'margin', 'misc']
    print('{:>17}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format('time', 'pair', 'type', 'price', 'cost', 'fee', 'vol'))
    for val in table:
        time = datetime.datetime.fromtimestamp(int(val[3]))
        print('{:%x %X}|{:>15}|{:>15}|{:>15.2f}|{:>15.2f}|{:>15.2f}|{:>15.2f}|'.format(time, val[2], val[4], float(val[6]), float(val[7]), float(val[8]), float(val[9])))


def print_position_table(table):
    print('{:<3}|{:>15}|{:>15}|'.format('#', 'currence', 'amount'))
    #print('{:<3}|{:>15}|{:>15}|{:>15}|'.format('#', 'currence', 'amount', 'amount (usd)'))
    count = 0
    for val in table:
        print('{:<3d}|{:>15}|{:>15.2f}|'.format(count, val[0], float(val[1])))
        #print('{:<3d}|{:>15}|{:>15.2f}|{:>15.2f}'.format(count, val[0], float(val[1]), val[2]))
        count += 1


def graph(prices):
    df = pd.DataFrame.from_dict(prices)
    df = pd.DataFrame(df, columns={'Price', 'Time'})
    df.plot(x='Time', y='Price')
    plt.show()


def print_open_position(position):
    print('Current positions:')
    for asset in position['result']:
        number = f"{float(position['result'][asset]):<-5}"
        text = '{:<4s}{:<2s}{:s}'
        print(text.format(asset, ':', number))


def print_order(order):
    for i in order:
        if i == 'time':
            date = ctime(float(order[i]))
            print(i, ': ', date, sep='')
        else:
            print(i, ': ', order[i], sep='')


def find_time(time):
    date = utils.parsedate_to_datetime(time)
    # date.strftime('%d/%b/%Y')
    return date.strftime('%H:%M')


def get_candle_graph(price):
    data=[go.Candlestick(x=price['time'],
        open=price['open'],
        high=price['high'],
        low=price['low'],
        close=price['close'])
        ]
    figSignal = go.Figure(data=data)
    figSignal.show()


def some_graph(data):
    # construct the figure

    fig = go.Figure(data=[go.Candlestick(x=data['time'],
                                         open=data['open'], high=data['high'],
                                         low=data['low'], close=data['close'])])
    # display our graph
    fig.show()
