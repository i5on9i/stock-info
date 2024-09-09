

import enum


class MarketTicker(enum.Enum):
    KOSPI = ('^KS11', 'Kospi')
    KOSDAQ = ('^KQ11', 'Kosdaq')
    SAMSUNG_ELECTRONICS = ('005930.KS', 'Samsung Electronics')

    DOW = ('^DJI', 'Dow Jones Industrial Average')
    MICROSOFT = ('MSFT', 'Microsoft')

    def __init__(self, value, label):
        self._value_ = value
        self._label = label

    @property
    def value(self):
        return self._value_
    
    @property
    def label(self):
        return self._label