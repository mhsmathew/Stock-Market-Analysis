import pandas_datareader as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# -------------------- Getting the data --------------------
stock = 'SPY'
# 12 months ago
start_time = (datetime.date.today() - datetime.timedelta(12*365/12)).isoformat()
#Today
end_time = datetime.datetime.today()
#data = pdr.get_data_yahoo(stock, start=start_time, end=end_time)
data = pdr.DataReader(stock, 'yahoo', start_time, end_time)

# -------------- Simple Moving Average Algorithm ---------------
# Short moving average
short_window = 20
# Long moving average
long_window = 100

indicators = pd.DataFrame(index=data.index)
indicators['price'] = data['Adj Close']
indicators['signal'] = 0.0

# Short window average over the data period
indicators['short_avg'] = data['Close'].rolling(window = short_window, min_periods = 1, center = False).mean()

# Long window average over the data period
indicators['long_avg'] = data['Close'].rolling(window = long_window, min_periods = 1, center = False).mean()

# Where they cross
indicators['signal'][short_window:] = np.where(
        indicators['short_avg'][short_window:] > indicators['long_avg'][short_window:],
        1.0, 0.0)

# Buy vs Sell
indicators['positions'] = indicators['signal'].diff()



print(indicators.loc[indicators['positions']**2 == 1])

# -------------------- Plotting -------------------------

# Create the plot
fig = plt.figure(figsize=(13,10))

# Labels for plot
ax1 = fig.add_subplot(111,  ylabel='Price in $')

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


