# Пример стратегии с использованием индикатора indicator_rs.RSIndricator


import backtrader as bt  # Импортируем backtrader

from indicator_rs import RSIndricator as rs  # Импортируем реализованный инидкатор


class St(bt.Strategy):
    '''
    Пример простой стратегии для тестирования реализованного индикатора RSIndricator
    '''
    def __init__(self):
        pass
