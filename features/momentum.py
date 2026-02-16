import pandas as pd
import numpy as np
import yfinance as yf
import fastparquet
import matplotlib.pyplot as plt


# this should calculate the simple last 10 day momentum
def calculate_momentum(file_data_name,window_horizon):
    dataframe = pd.read_parquet(file_data_name)
    for num in range(0,window_horizon):
        dataframe = dataframe + dataframe.shift(1)
    
    return dataframe
        
        
# frame = calculate_momentum("../data/return1day.parquet",9)

# frame.to_parquet("1../data/0daymomentum.parquet",engine = "pyarrow",compression= "snappy")

# frame = calculate_momentum("../data/return1day.parquet",21)

# frame.to_parquet("../data/21daymomentum.parquet",engine = "pyarrow",compression= "snappy")

# frame = calculate_momentum("../data/return1day.parquet",63)

# frame.to_parquet("../data/63daymomentum.parquet",engine = "pyarrow",compression= "snappy")