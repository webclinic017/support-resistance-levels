import pandas as pd

from pricelevels.cluster import RawPriceClusterLevels

df = pd.read_csv('orcl-1995-2014.txt')
cl = RawPriceClusterLevels(None, merge_percent=0.25, use_maximums=True, bars_for_peak=91)
cl.fit(df)
levels = cl.levels


for i in levels:
    print(i)
