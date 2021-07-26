import time
from email import utils
import DataCollection as dc
import DataOutput as do


def find_time(time):
    date = utils.parsedate_to_datetime(time)
    #date.strftime('%d/%b/%Y')
    return date.strftime('%H:%M')


def get_price_period(pair, period):
    timestamps = []
    prices = []
    t_end = time.time() + 60 * period
    previous_price = 0
    while time.time() < t_end:
        current_price = float(dc.get_current_price(pair))
        timestamp = find_time(time.asctime(time.localtime(time.time())))
        if current_price != previous_price and current_price > 0:
            timestamps.append(timestamp)
            prices.append(current_price)
        previous_price = current_price
    time_and_price = {'Time': timestamps, 'Price': prices}
    return time_and_price


def get_open_positions():
    position = dc.get_current_positions()
    do.open_position(position)


if __name__ == '__main__':
    start_time = time.time()

    # dictionary, key([time]) -> value([price])
    #quotations = get_price_period('ETHUSDT', 0.1)
    # to show a price graph
    #do.get_graph(quotations)

    get_open_positions()

    #print("Balance:", dc.get_current_balance('USD'))
    print("--- %s seconds ---" % (time.time() - start_time))
