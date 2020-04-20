import pandas_datareader as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


class movingAverages:
    def __init__(self, stock, average_type):
        self.indicators = None
        self.stock = stock
        # -------------------- Options --------------------
        # Short moving average
        self.short_window = 50
        # Long moving average
        self.long_window = 200

        # Simple or Exponential Moving Average
        self.average_type = average_type
        # Window time period in months
        month_window = 10

        # -------------------- Getting the data --------------------
        # self.start_time = (datetime.date.today() - datetime.timedelta(month_window * 365 / 12)).isoformat()
        self.start_time = datetime.datetime(2014, 1, 1)
        # Today
        self.end_time = datetime.datetime.today()
        # self.end_time = datetime.datetime(2020, 1, 28)
        # data = pdr.get_data_yahoo(stock, start=start_time, end=end_time)
        self.data = pdr.DataReader(stock, 'yahoo', self.start_time, self.end_time)

    def get_positions(self):
        # -------------- Moving Average Algorithm ---------------
        indicators = pd.DataFrame(index=self.data.index)
        indicators['price'] = self.data['Adj Close']
        indicators['signal'] = 0.0

        # Short and long window average over the data period
        if self.average_type == "simple":

            indicators['short_avg'] = self.data['Close'].rolling(window=self.short_window, min_periods=1,
                                                                 center=False).mean()
            indicators['long_avg'] = self.data['Close'].rolling(window=self.long_window, min_periods=1,
                                                                center=False).mean()
        elif self.average_type == "exponential":
            indicators['short_avg'] = self.data['Close'].ewm(span=self.short_window, adjust=False).mean()
            indicators['long_avg'] = self.data['Close'].ewm(span=self.long_window, adjust=False).mean()

        # Where they cross
        indicators['signal'][self.short_window:] = np.where(
            indicators['short_avg'][self.short_window:] > indicators['long_avg'][self.short_window:],
            1.0, 0.0)

        # Buy vs Sell
        indicators['positions'] = indicators['signal'].diff()
        self.indicators = indicators
        return indicators.loc[indicators['positions'] ** 2 == 1]

    def get_time(self):
        return self.start_time, self.end_time

    def get_data(self):
        return self.data

    def plot(self):
        # -------------------- Plotting -------------------------
        # Get data from object
        indicators = self.indicators
        data = self.data
        # Create the plot
        fig = plt.figure(figsize=(13, 10))

        # Labels for plot
        ax1 = fig.add_subplot(111, ylabel='Price in $')

        # Plot stock price over time
        data['Close'].plot(ax=ax1, color='black', lw=2.)

        # Plot the the short and long moving averages
        indicators[['short_avg', 'long_avg']].plot(ax=ax1, lw=2.)

        # Plot where to buy indicators
        ax1.plot(indicators.loc[indicators.positions == 1.0].index,
                 indicators.short_avg[indicators.positions == 1.0],
                 '^', markersize=10, color='g')

        # Plots where to sell indicators
        ax1.plot(indicators.loc[indicators.positions == -1.0].index,
                 indicators.short_avg[indicators.positions == -1.0],
                 'v', markersize=10, color='r')

        # Show the plot
        plt.show()
