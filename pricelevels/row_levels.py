import pandas as pd

from pricelevels.cluster import RawPriceClusterLevels
from pricelevels.visualization.levels_on_candlestick import plot_levels_on_candlestick

# Сухой остаток из изначального проекта.
# Все что ниже обернуть в функцию и вызывать с 4 аргументами:
# 1. candles или файл со свечами
# 2. merge_percent
# 3. use_maximum
# 4. bars_for_peak
# На выход отдается массив кластеров:
# [{'cluster': 0, 'price': 3.796875, 'peak_count': 2}, ... , {'cluster': 34, 'price': 2.962963, 'peak_count': 1}]

df = pd.read_csv('orcl-1995-2014.txt')
cl = RawPriceClusterLevels(None, merge_percent=1, use_maximums=True, bars_for_peak=91)
cll = RawPriceClusterLevels(None, merge_percent=1, use_maximums=False, bars_for_peak=91)
cl.fit(df)
cll.fit(df)
levels = cl.levels
levelsd = cll.levels

print('TOP:')
for i in levels:
    print(i)

print('BOT:')
for i in levelsd:
    print(i)

plot_levels_on_candlestick(df, levels, only_good=False)  # in case you want to display chart
plot_levels_on_candlestick(df, levelsd, only_good=False)  # in case you want to display chart