import matplotlib.pyplot as plt
from time import ctime
from email import utils
import pandas as pd
import shrimpy
import plotly.graph_objects as go


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
