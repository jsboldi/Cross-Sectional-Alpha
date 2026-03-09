import pandas as pd
import numpy as np
import yfinance as yf
import fastparquet
import matplotlib.pyplot as plt

#this file will calculate returns for 1 day 5 day and 20 day and create parquet files for all as well

dataframe = pd.read_parquet("../data/data.parquet",engine= 'pyarrow')

dataframe_1day_return = np.log(dataframe/dataframe.shift(1))
print(dataframe_1day_return)

dataframe_5day_return = np.log(dataframe/dataframe.shift(5))


dataframe_20day_return = np.log(dataframe/dataframe.shift(20))


print(dataframe_1day_return.info())
print("Any <= 0 prices?", (dataframe_1day_return <= 0).any().any())
print("Count <= 0 prices:", (dataframe_1day_return <= 0).sum().sum())
print("NaN count:", dataframe_1day_return.isna().sum().sum())
print(dataframe_5day_return.info())
print("Any <= 0 prices?", (dataframe_5day_return <= 0).any().any())
print("Count <= 0 prices:", (dataframe_5day_return <= 0).sum().sum())
print("NaN count:", dataframe_5day_return.isna().sum().sum())
print(dataframe_20day_return.info())
print("Any <= 0 prices?", (dataframe_20day_return <= 0).any().any())
print("Count <= 0 prices:", (dataframe_20day_return <= 0).sum().sum())
print("NaN count:", dataframe_20day_return.isna().sum().sum())

# dataframe_1day_return.to_parquet('../data/return1day.parquet', engine = 'pyarrow',compression= 'snappy')
# dataframe_5day_return.to_parquet('../data/return5day.parquet', engine = 'pyarrow',compression= 'snappy')
# dataframe_20day_return.to_parquet('../data/return20day.parquet', engine = 'pyarrow',compression= 'snappy')