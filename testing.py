import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 5, None, 3, 7]})
df2 = pd.DataFrame({'a': [1, 2, 4], 'c': [None, None, 9]})
df3 = pd.DataFrame({'a': [1, 3, 4, 5], 'd': [None, 11, 12, 13]})

merge_df = pd.merge(df1, df2[['a','c']], on='a', how='left')
# merge_df = pd.merge(df1, df3, on='a', how='left')
# print(np.where(((df1.a==1)&(df2.a==1))))
print(merge_df)