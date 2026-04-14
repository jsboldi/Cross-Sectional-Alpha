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
    






def calculate_volatility(filename, numdays):
    dataframe = pd.read_parquet(filename,engine="pyarrow")
    print(dataframe.head())
    vol_frame = pd.DataFrame(index=dataframe.index, columns=dataframe.columns, dtype = np.float32)

    for column in dataframe.columns:

        num_entries = len(dataframe[column])
        
        ticker_vol = []
        for j in range(0,num_entries):
            if j >= numdays-1:
                window = dataframe[column].iloc[j-(numdays-1):j+1]
                vol_value = compute_individual_volatility(window)
            else:
                vol_value = 0
            ticker_vol.append(vol_value)
            
        
        vol_frame[column] = ticker_vol

      
       
        
        
    return vol_frame








    
# uncomment to download the data
vol_frame5 = calculate_volatility("../data/return1day.parquet",5)
vol_frame20 = calculate_volatility("../data/return1day.parquet",20)
vol_frame63 = calculate_volatility("../data/return1day.parquet",63)
#vol_frame = vol_frame.stack()



    
vol_frame5.to_parquet('../data/volatility5d.parquet', engine = 'pyarrow',compression= 'snappy')
vol_frame20.to_parquet('../data/volatility20d.parquet', engine = 'pyarrow',compression= 'snappy')
vol_frame63.to_parquet('../data/volatility63d.parquet', engine = 'pyarrow',compression= 'snappy')