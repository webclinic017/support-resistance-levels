# Индикатор для фреймворка Backtrader - Линии поддержки и сопротивления


import backtrader as bt  # Импортируем backtrader


class RSIndricator(bt.Indicator):
    '''
    Класс индикатора линиий поддержки и сопротивления Backtrader
    '''
    lines = ('support', 'resistance',)  # indicator's lines

    def __init__(self, bars_count: int, rs_distance: float, date_back_range: int):
        '''
        :param bars_count: количество архивных свечей для построения индикатора
        :param rs_distance: дельта расстояния между экстремумами (насколько близки должны быть точки, чтобы считались одним уровнем)
        :param date_back_range: ограничение по сроку в прошлое (нужно 100 баров, есть ли они в пределах 2х дней, если нет, взять меньше баров)
        '''
        self.bars_count = bars_count
        self.rs_distance = rs_distance
        self.date_back_range = date_back_range
