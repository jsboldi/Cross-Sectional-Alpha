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
    vol_frame = pd.DataFrame(columns=dataframe.columns)
    for column in dataframe.columns:
        j = 0
        stock_vol_list = []
        for rtn in dataframe[column]:
            #  we want to calulcate each return in the sliding windows squared difference of the mean
            # if j >= 20 :
            #     dataframe['column'][j:j-19]
            if j > 19:
                stock_vol_list.append(compute_individual_volatility(dataframe[column][j-19:j]))
            j = j + 1
            
        vol_frame[column] = stock_vol_list
    return vol_frame



    
# uncomment to download the data
# vol_frame = calculate_volatility("return1day.parquet")
    
# vol_frame.to_parquet('volatility.parquet', engine = 'pyarrow',compression= 'snappy')

