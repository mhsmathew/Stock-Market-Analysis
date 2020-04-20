from Get_Data import GetData
import pandas as pd

# Tests our model with the top 50 S&P Stocks
stock_training =["MSFT", "AAPL", "AMZN", "GOOG", "FB", "JNJ", "WMT", "V", "PG", "JPM", "UNH", "MA", "INTC", "VZ", "HD", "T", "MRK", "KO", "PFE", "BAC", "DIS", "PEP", "NFLX", "XOM", "CSCO", "NVDA", "CMCSA", "ORCL", "ABT", "ADBE", "CVX", "LLY", "CRM", "COST", "NKE", "TSLA", "MDT", "MCD", "AMGN", "BMY", "PYPL", "TMO", "ABBV", "PM", "NEE", "CHTR", "WFC", "ACN", "LMT"]
# Aggregates data into a list of dataframes
data_frames=[]
for stock in stock_training:
    print(stock, "Gathering")
    data_frames.append(GetData(stock).prepare_data_for_training())
    # Error in one of stocks
    if data_frames[-1].isnull().sum().sum() > 0:
        print(stock, "NULL")
    print(stock, "Success")
# Combines all the data into 1 dataframe
data = pd.concat(data_frames, ignore_index=True)
# Outputs dataframe to csv
data.to_csv('data.csv', index=True)
