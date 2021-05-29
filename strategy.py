# Пример стратегии с использованием индикатора indicator_rs.RSIndricator


import backtrader as bt  # Импортируем backtrader

from indicator_rs import RSIndricator  # Импортируем реализованный инидкатор


class St(bt.Strategy):
    '''
    Пример простой стратегии для тестирования реализованного индикатора RSIndricator
    '''

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # RSIndicator
        self.rs = RSIndricator(bars_count=10, rs_distance=10.0, date_back_range=21)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('RSIndicator, %.2f' % self.rs[0])
