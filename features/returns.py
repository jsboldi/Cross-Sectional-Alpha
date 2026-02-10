import pandas as pd
import numpy as np
import yfinance as yf
import fastparquet
import matplotlib.pyplot as plt

#this file will calculate returns for 1 day 5 day and 20 day and create parquet files for all as well

dataframe = pd.read_parquet("../data/data.parquet",engine= 'pyarrow')

dataframe_1day_return = (dataframe/dataframe.shift(1)) - 1
print(dataframe_1day_return)

dataframe_5day_return = (dataframe/dataframe.shift(5)) - 1


dataframe_20day_return =(dataframe/dataframe.shift(20)) - 1



dataframe_1day_return.to_parquet('return1day.parquet', engine = 'pyarrow',compression= 'snappy')
dataframe_5day_return.to_parquet('return5day.parquet', engine = 'pyarrow',compression= 'snappy')
dataframe_20day_return.to_parquet('return20day.parquet', engine = 'pyarrow',compression= 'snappy')