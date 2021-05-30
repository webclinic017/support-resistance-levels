# Индикатор для фреймворка Backtrader - Линии поддержки и сопротивления
from random import random
import pandas as pd
import backtrader as bt  # Импортируем backtrader

from pricelevels.cluster import RawPriceClusterLevels


def convert_to_df(data):
    '''
    Convert backtrader Datafeed(datas) to Pandas DataFrame (format for RawPriceClusterLevels)
    :param data: data for converting (self.datas[0] - in Indicator)
    :return: data in pandas df
    '''
    # Process of preparing data
    rowData = pd.DataFrame(columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
    for i, candle in enumerate(data):
        # print(i)
        rowData = rowData.append({
            'Datetime': data.datetime.date(i),
            'Open': data.open[i],
            'High': data.high[i],
            'Low': data.low[i],
            'Close': data.close[i],
            'Volume': data.volume[i]
        }, ignore_index=True)

    return rowData

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

    def __init__(self):
        # self.csv_data = pd.read_csv('datas/orcl-1995-2014.txt')
        self.clsp = RawPriceClusterLevels(None, merge_percent=0.7, use_maximums=True, bars_for_peak=21)
        self.clrs = RawPriceClusterLevels(None, merge_percent=0.7, use_maximums=False, bars_for_peak=21)
        print('support resistance cnt')
        self.cnt = 0
        self.supportVal = 0
        self.resistVal = 0
        #self.lines.support[0] = 0
        #self.lines.resistance[0] = 0

    def next(self):
        df_data = convert_to_df(self.datas[0])
        self.clsp.fit(df_data)
        self.clrs.fit(df_data)
        self.cnt += 1
        if self.datas[0].close[-1] <= self.datas[0].open[-1]:
            highPrice = self.datas[0].open[-1]
            lowPrice = self.datas[0].close[-1]
        else:
            highPrice = self.datas[0].close[-1]
            lowPrice = self.datas[0].open[-1]
        if not(self.clsp.levels is None or self.clrs.levels is None):
            self.supportVal = min(v['price'] for v in self.clsp.levels
                                     if v['price'] >= highPrice)  # TODO: has to be redefined using RawPriceClusterLevels
            self.resistVal = max(v['price'] for v in self.clrs.levels
                                        if v['price'] <= lowPrice)  # TODO: has to be redefined using RawPriceClusterLevels

        self.lines.support[0] = self.supportVal
        self.lines.resistance[0] = self.resistVal
        print(str(self.lines.support[0]) + ' ' + str(self.lines.resistance[0]) + ' ' + str(self.cnt))
