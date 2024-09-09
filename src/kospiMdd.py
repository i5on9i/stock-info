"""

:ref : https://github.com/INVESTAR/StockAnalysisInPython/blob/master/03_NumPy_and_Pandas/ch03_01_KOSPI_MDD.py
"""

import yfinance as yf
import matplotlib.pyplot as plt
import argparse

from common.ticker import MarketTicker


class MDD:
    
    KOSDAQ = MarketTicker.KOSDAQ.name
    KOSPI = MarketTicker.KOSPI.name

    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.kospi = yf.download(MarketTicker.KOSPI.value, start=start_date, end=end_date)
        self.kosdaq = yf.download(MarketTicker.KOSDAQ.value, start=start_date, end=end_date)

    @property
    def window(self):
        return 252 # about an year

    @property
    def peak(self):
        return self.kospi['Adj Close'].rolling(self.window, min_periods=1).max()
    
    @property
    def drawdown(self):
        return self.kospi['Adj Close'] / self.peak - 1.0

    @property
    def max_dd(self):
        return self.drawdown.rolling(self.window, min_periods=1).min()

    def getPeak(self, series):
        return series['Adj Close'].rolling(window=self.window, min_periods=1).max()
    
    def getDrawdown(self, series):
        return series['Adj Close'] / self.getPeak(series) - 1.0
    
    def getMaxDD(self, series):
        return self.getDrawdown(series).rolling(window=self.window, min_periods=1).min()
    
    def plot(self):

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 9))
        self.kospi['Close'].plot(ax=ax1, label=self.KOSPI, title=f'{self.KOSPI} MDD', grid=True, legend=True)
        self.kosdaq['Close'].plot(ax=ax3, label=self.KOSDAQ, title=f'{self.KOSDAQ} MDD', grid=True, legend=True)

        self.getDrawdown(self.kospi).plot(ax=ax2, c='blue', label=f'{self.KOSPI} DD', grid=True, legend=True)
        self.getMaxDD(self.kospi).plot(ax=ax2, c='red', label=f'{self.KOSPI} MDD', grid=True, legend=True)
        self.getDrawdown(self.kosdaq).plot(ax=ax2, c='green', label=f'{self.KOSDAQ} DD', grid=True, legend=True)

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', '-t', default='^KS11', help='ticker')
    parser.add_argument('--start', '-s', default='2019-01-01', help='start date')
    parser.add_argument('--end', '-e', default='2019-12-31', help='end date')
    args = parser.parse_args()

    mdd = MDD(args.ticker, args.start, args.end)
    mdd.plot()
