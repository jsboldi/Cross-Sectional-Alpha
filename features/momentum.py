import pandas as pd
import numpy as np
import yfinance as yf
import fastparquet
import matplotlib.pyplot as plt


# this should calculate the simple last 10 day momentum
def calculate_momentum(file_data_name,window_horizon):
    dataframe = pd.read_parquet(file_data_name)
    df = dataframe


    print("Any <= 0 prices?", (df <= 0).any().any())
    print("Count <= 0 prices:", (df <= 0).sum().sum())
    print("NaN count:", df.isna().sum().sum())

    x = np.log(df)
    print("Inf count after log:", np.isinf(x.to_numpy()).sum())
    print("NaN count after log:", np.isnan(x.to_numpy()).sum())
    df.reset_index()
    print(df.info())
    dataframe = np.log(dataframe/dataframe.shift(window_horizon))
    return dataframe
        
        
frame = calculate_momentum("../data/return1day.parquet",9)

frame.to_parquet("../data/10daymomentum.parquet",engine = "pyarrow",compression= "snappy")

frame = calculate_momentum("../data/return1day.parquet",21)

frame.to_parquet("../data/21daymomentum.parquet",engine = "pyarrow",compression= "snappy")

frame = calculate_momentum("../data/data.parquet",63)

print(frame.info())

frame.to_parquet("../data/63daymomentum.parquet",engine = "pyarrow",compression= "snappy")