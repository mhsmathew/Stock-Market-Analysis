from Moving_Average import movingAverages

def back_test(data, indicators):
    num_buy = len(indicators.loc[indicators.positions == 1.0])
    num_sell = len(indicators.loc[indicators.positions == -1.0])
    total_buy = sum(indicators.loc[indicators.positions == 1.0]['price'])
    total_sell = sum(indicators.loc[indicators.positions == -1.0]['price'])
    if num_buy != num_sell:
        # In case there was no sell indicator, so now profit is current value of stock
        total_buy += data['Close'][-1]
    total_profit_trading = total_sell - total_buy + (num_buy - num_sell)
    total_profit_holding = data['Close'][-1] - data['Close'][0]
    percent_increase = 100 * (total_profit_trading - total_profit_holding) / total_profit_holding

    print('\n------ Data With Swing Trading ------')
    print('Profit = ' + str(round(total_profit_trading, 2)))

    print('\n------ Just Buy and Hold ------')
    print('Profit  = ' + str(round(total_profit_holding, 2)))

    print('\n------ Analysis ------')
    print('Time in years spend trading = ' + str(round((p.get_time()[1] - p.get_time()[0]).days / 365, 2)))
    print('Trades made = ' + str(num_buy + num_sell))
    print('Price of Stock =  ' + str(data['Close'][0]) + ' now at ' + str(data['Close'][-1]))
    print('Swing Trading did ' + str(round(percent_increase, 2)) + '% better than holding')
    return percent_increase


# -------------------- data importing and back testing -------------------------
stock = "T"
print('\n---------- Simple Moving Average Crossover -----------')
p = movingAverages(stock, "simple")
indicators = p.get_positions()
data = p.get_data()
print(str(back_test(data, indicators)) + "%")
print('\n---------- Exponential Moving Average Crossover -----------')
p = movingAverages(stock, "exponential")
indicators = p.get_positions()
data = p.get_data()
print(str(back_test(data, indicators)) + "%")
p.plot()
