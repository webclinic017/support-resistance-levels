import pandas as pd

from pricelevels.cluster import RawPriceClusterLevels

# Сухой остаток из изначального проекта.
# Все что ниже обернуть в функцию и вызывать с 4 аргументами:
# 1. candles или файл со свечами
# 2. merge_percent
# 3. use_maximum
# 4. bars_for_peak
# На выход отдается массив кластеров:
# [{'cluster': 0, 'price': 3.796875, 'peak_count': 2}, ... , {'cluster': 34, 'price': 2.962963, 'peak_count': 1}]

df = pd.read_csv('orcl-1995-2014.txt')
cl = RawPriceClusterLevels(None, merge_percent=0.25, use_maximums=True, bars_for_peak=91)
cl.fit(df)
levels = cl.levels


for i in levels:
    print(i)
