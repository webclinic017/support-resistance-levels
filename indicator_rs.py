# Индикатор для фреймворка Backtrader - Линии поддержки и сопротивления


import backtrader as bt  # Импортируем backtrader
from pricelevels.cluster import RawPriceClusterLevels


class RSIndricator(bt.Indicator):
    '''
    Класс индикатора линиий поддержки и сопротивления Backtrader
    '''
    lines = ('support', 'resistance',)  # indicator's lines

    params = (
        ('bars_count', 10),
        ('rs_distance', 10),
        ('date_back_range', 10),
    )
    #:param bars_count: количество архивных свечей для построения индикатора
    #:param rs_distance: дельта расстояния между экстремумами (насколько близки должны быть точки, чтобы считались одним уровнем)
    #:param date_back_range: ограничение по сроку в прошлое (нужно 100 баров, есть ли они в пределах 2х дней, если нет, взять меньше баров)

    plotinfo = dict(subplot=False)  # Для отрисовки Индикатора на основном графике

    def next(self):
        self.lines.support[0] = 25  # TODO: has to be redefined using RawPriceClusterLevels
        self.lines.resistance[0] = 35  # TODO: has to be redefined using RawPriceClusterLevels
