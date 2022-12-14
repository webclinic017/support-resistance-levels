# Индикатор для фреймворка Backtrader - Линии поддержки и сопротивления
import datetime
from random import random
import pandas as pd
import backtrader as bt  # Импортируем backtrader

from pricelevels.cluster import RawPriceClusterLevels


def cut_and_convert_to_df(data, size):
    '''
    Convert backtrader Datafeed(datas) to Pandas DataFrame (format for RawPriceClusterLevels)
    :param size: size of a new dataset
    :param data: data for converting (self.datas[0] - in Indicator)
    :return: cuted data in pandas df
    '''
    # Process of preparing data
    rowData = pd.DataFrame(columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
    dataAsDict = dict()
    dataAsDict['open'] = data.open.get(size=size)
    dataAsDict['high'] = data.high.get(size=size)
    dataAsDict['low'] = data.low.get(size=size)
    dataAsDict['close'] = data.close.get(size=size)
    dataAsDict['volume'] = data.volume.get(size=size)
    dataAsDict['datetime'] = data.datetime.get(size=size)

    n = len(data.get(size=size))
    if n == 0:
        return rowData

    for i in range(n):
        rowData = rowData.append({
            'Datetime': datetime.date.fromordinal(int(dataAsDict['datetime'][i])),
            'Open': dataAsDict['open'][i],
            'High': dataAsDict['high'][i],
            'Low': dataAsDict['low'][i],
            'Close': dataAsDict['close'][i],
            'Volume': dataAsDict['volume'][i]
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
        self.clsp = RawPriceClusterLevels(None, merge_percent=0.7, use_maximums=True, bars_for_peak=3)
        self.clrs = RawPriceClusterLevels(None, merge_percent=0.7, use_maximums=False, bars_for_peak=3)
        print('support resistance cnt')
        self.cnt = 0
        self.supportVal = 0
        self.resistVal = 0

        self.prev_rs = []
        self.prev_sp = []
        # self.lines.support[0] = 0
        # self.lines.resistance[0] = 0

    def next(self):
        df_data = cut_and_convert_to_df(self.data, 10)
        if df_data.size == 0:
            return

        self.clsp.fit(df_data)
        self.clrs.fit(df_data)

        self.cnt += 1
        closePrice = self.datas[0].close[-1]

        if not (self.clsp.levels is None or self.clrs.levels is None):
            arr_sp = []
            for v in self.prev_sp:
                if v['price'] >= closePrice:
                    arr_sp.append(v['price'])
            if len(arr_sp) != 0:
                self.lines.support[0] = min(arr_sp)
            else:
                self.lines.support[0] = self.supportVal

            arr_rs = []
            for v in self.prev_rs:
                if v['price'] <= closePrice:
                    arr_rs.append(v['price'])
            if len(arr_rs) != 0:
                self.lines.resistance[0] = max(arr_rs)
            else:
                self.lines.resistance[0] = self.resistVal

            self.prev_rs = self.clrs.levels
            self.prev_sp = self.clsp.levels
        else:
            arr_sp = []
            for v in self.prev_sp:
                if v['price'] >= closePrice:
                    arr_sp.append(v['price'])

            if len(arr_sp) != 0:
                self.lines.support[0] = min(arr_sp)
            else:
                self.lines.support[0] = self.supportVal

            arr_rs = []
            for v in self.prev_rs:
                if v['price'] <= closePrice:
                    arr_rs.append(v['price'])

            if len(arr_rs) != 0:
                self.lines.resistance[0] = max(arr_rs)
            else:
                self.lines.resistance[0] = self.resistVal

        print(str(self.lines.support[0]) + ' ' + str(self.lines.resistance[0]) + ' ' + str(self.cnt))
