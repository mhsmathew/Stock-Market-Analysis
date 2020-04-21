import pandas_datareader as pdr
import pandas as pd
import datetime
import math
from finta import TA


class GetData:
    def __init__(self, stock, just_today=False):
        self.just_today = just_today
        # 500 months of data
        self.start_time = (datetime.date.today() - datetime.timedelta(500 * 365 / 12)).isoformat()
        if self.just_today:
            # Limiting unneeded computations, may need old data from some indicators
            self.start_time = (datetime.date.today() - datetime.timedelta(5 * 365 / 12)).isoformat()
        # Today
        self.end_time = datetime.datetime.today()
        self.data = pdr.DataReader(stock, 'yahoo', self.start_time, self.end_time)
        # Getting the S&P500 relative price difference. A 5% gain is not impressive, if S&P gained 10%
        SP = pdr.DataReader('SPY', 'yahoo', self.start_time, self.end_time)
        SP['sp_percent_change'] = SP['Adj Close'].pct_change(periods=1).astype(float)
        self.data = self.data.merge(SP['sp_percent_change'], left_index=True, right_index=True)
        self.data['percent_change'] = self.data['Adj Close'].pct_change(periods=1).astype(float)
        # Daily percent change as compared to the S&P500
        self.data['relative_change'] = self.data['percent_change'] - self.data['sp_percent_change']
        self.data.reset_index(inplace=True)
        self.data.columns = [x.lower() for x in self.data.columns]

    def get_data(self):
        return self.data

    # Adds indicators to dataframe of this given stock
    def add_indicators(self):
        # This is a list of all possible indicators we can use
        # indicators = ['ADL', 'ADX', 'AO', 'APZ', 'ATR',
        # 'BASP', 'BASPN', 'BBANDS', 'BBWIDTH', 'CCI', 'CFI', 'CHAIKIN', 'CHANDELIER', 'CMO', 'COPP', 'DEMA', 'DMI',
        # 'DO', 'EBBP', 'EFI', 'EMA', 'EMV', 'ER', 'EVWMA', 'EV_MACD', 'FISH', 'FVE', 'HMA', 'ICHIMOKU', 'IFT_RSI',
        # 'KAMA', 'KC', 'KST', 'MACD', 'MFI', 'MI', 'MOM', 'MSD', 'OBV', 'PERCENT_B', 'PIVOT', 'PIVOT_FIB', 'PPO',
        # 'PZO', 'QSTICK', 'ROC', 'RSI', 'SAR', 'SMA', 'SMM', 'SMMA', 'SQZMI', 'SSMA', 'STC', 'STOCH', 'STOCHD',
        # 'STOCHRSI', 'TEMA', 'TMF', 'TP', 'TR', 'TRIMA', 'TRIX', 'TSI', 'UO', 'VAMA', 'VFI', 'VORTEX', 'VPT', 'VR',
        # 'VWAP', 'VW_MACD', 'VZO', 'WILLIAMS', 'WMA', 'WOBV', 'WTO', 'ZLEMA']

        # Here are all indicators we are using
        indicators = ['SMA', 'SMM', 'SSMA', 'EMA', 'DEMA', 'TEMA', 'TRIMA', 'TRIX', 'VAMA', 'ER', 'KAMA', 'ZLEMA',
                      'WMA', 'HMA', 'EVWMA', 'VWAP', 'SMMA', 'MACD', 'PPO', 'VW_MACD', 'EV_MACD', 'MOM', 'ROC', 'RSI',
                      'IFT_RSI']
        # These indicators need more tuning or are broken
        broken_indicators = ['SAR', 'TMF', 'VR', 'QSTICK']
        for indicator in indicators:
            if indicator not in broken_indicators:
                df = None
                # Using python's eval function to create a method from a string instead of having every method defined
                df = eval('TA.' + indicator + '(self.data)')
                # Some method return series, so we can check to convert here
                if not isinstance(df, pd.DataFrame):
                    df = df.to_frame()
                # Appropriate labels on each column
                df = df.add_prefix(indicator + '_')
                # Join merge dataframes based on the date
                self.data = self.data.merge(df, left_index=True, right_index=True)
        # Fix labels
        self.data.columns = self.data.columns.str.replace(' ', '_')

    # Prepares our dataframe for training
    def prepare_data_for_training(self):
        self.add_indicators()
        self.data = self.get_data()
        self.add_short_testing()
        if not self.just_today:
            # Some indicators need longer time so we can just remove first 500
            self.data = self.data[500:]
            # In order to accurately train on future success we need to eliminate not fully completed entries
            self.data = self.data[:-30]
        else:
            self.data = self.data.tail(1)
        return self.data

    # Adds short term stock results in relation to current position
    def add_short_testing(self):
        # We will use short term as being 1 day to 30 days
        self.data['short_result'] = None
        for index, row in self.data.iterrows():
            # Sums the total relative change compared to S&P over
            percent_change = self.data.loc[index + 1:index + 30]['relative_change'].sum() * 100
            # Need for our model
            if math.isnan(percent_change):
                percent_change = 0
            else:
                percent_change = int(round(percent_change))
            self.data.at[index, 'short_result'] = percent_change
        del self.data['relative_change']
