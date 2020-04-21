from Stock_List import Access_Tickers
from Get_Data import GetData
import pandas as pd

tickers = Access_Tickers().get_stocks()
data_frames = []
for ticker in tickers:
    print(ticker)
    t=GetData(ticker, True).prepare_data_for_training()
    t['ticker']=ticker
    data_frames.append(t)
    # Will add
pd.concat(data_frames, ignore_index=True).to_csv('today.csv', index=True)
