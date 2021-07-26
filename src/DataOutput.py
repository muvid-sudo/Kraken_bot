import matplotlib.pyplot as plt
import pandas as pd


def get_graph(prices):
    df = pd.DataFrame.from_dict(prices)
    df = pd.DataFrame(df, columns={'Price', 'Time'})
    df.plot(x='Time', y='Price')
    plt.show()
