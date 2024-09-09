

import yfinance as yf
from common.ticker import MarketTicker
import matplotlib.pyplot as plt

class DailyPercentageChange:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = yf.download(ticker, start=start, end=end)
    
    @property
    def cumsum(self):
        closePrice = self.data['Close']
        price1DayAgo = closePrice.shift(1)
        dpc = (closePrice / price1DayAgo - 1) * 100 # (closePrice - price1DayAgo) / price1DayAgo * 100
        dpc.iloc[0] = 0 
        return dpc.cumsum()

class IndexedStockPrice:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = yf.download(ticker, start=start, end=end)
    
    @property
    def indexedPrice(self):
        closePrice = self.data['Close']
        basePrice = self.data['Close'].iloc[0]
        indexedValues = (closePrice / basePrice - 1) * 100
        return indexedValues


if __name__ == '__main__':

    samsungElecDPC = DailyPercentageChange(MarketTicker.SAMSUNG_ELECTRONICS.value, '2019-01-01', '2024-12-31')
    microsoftDPC = DailyPercentageChange(MarketTicker.MICROSOFT.value, '2019-01-01', '2024-12-31')

    plt.plot(samsungElecDPC.data.index, samsungElecDPC.cumsum, 'b', label = MarketTicker.SAMSUNG_ELECTRONICS.label)
    plt.plot(microsoftDPC.data.index, microsoftDPC.cumsum, 'r--', label = MarketTicker.MICROSOFT.label)

    samsungElec = IndexedStockPrice(MarketTicker.SAMSUNG_ELECTRONICS.value, '2019-01-01', '2024-12-31')
    microsoft = IndexedStockPrice(MarketTicker.MICROSOFT.value, '2019-01-01', '2024-12-31')

    plt.plot(samsungElec.data.index, samsungElec.indexedPrice, color = '#2E8BC0', label = f'{MarketTicker.SAMSUNG_ELECTRONICS.label} Index')
    plt.plot(microsoft.data.index, microsoft.indexedPrice, color = '#ef7c8e', linestyle = '--', label = f'{MarketTicker.MICROSOFT.label} Index')

    plt.ylabel('Change %')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()

