import pandas as pd
import numpy as np
import yfinance as yf
import fastparquet
import matplotlib.pyplot as plt
import math


def compute_individual_volatility(numlist):
    i = 0
    sum = 0
    mean_squared_diff_sum = 0
    for num in numlist:
        sum = sum + num
        i = i + 1
        
    mean = sum / i
    
    for num in numlist:
        mean_squared_diff_sum = mean_squared_diff_sum + pow(num-mean,2)
        
   
        
    std_dev  = math.sqrt(mean_squared_diff_sum/(i-1))
        
    return std_dev
    






def calculate_volatility(filename):
    dataframe = pd.read_parquet(filename,engine="pyarrow")
    print(dataframe.head())
    vol_frame = pd.DataFrame(index=dataframe.index, columns=dataframe.columns, dtype = np.float32)

    for column in dataframe.columns:

        num_entries = len(dataframe[column])
        
        ticker_vol = []
        for j in range(0,num_entries):
            if j >= 19:
                window = dataframe[column].iloc[j-19:j+1]
                vol_value = compute_individual_volatility(window)
            else:
                vol_value = 0
            ticker_vol.append(vol_value)
            
        
        vol_frame[column] = ticker_vol

      
       
        
        
    return vol_frame








    
# uncomment to download the data

vol_frame = calculate_volatility("../data/return1day.parquet")
#vol_frame = vol_frame.stack()

print(vol_frame.tail(200))

    
vol_frame.to_parquet('../data/volatility.parquet', engine = 'pyarrow',compression= 'snappy')

