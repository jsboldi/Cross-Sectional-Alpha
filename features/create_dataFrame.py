import volatility
import momentum
import pandas as pd
import numpy as np




def create_dataframe():
    dataframe = pd.DataFrame(columns=["Date","Ticker","5dayReturn","63dayMomentum","20dayVolatility","Forward return"])
    
    return dataframe


def load_all_data(dataframe):
    rtn_df = pd.read_parquet("../data/return5day.parquet",engine = "pyarrow")
    vol_df = pd.read_parquet("../data/volatility.parquet", engine = "pyarrow")
    mom_df = pd.read_parquet("../data/63daymomentum.parquet",engine = "pyarrow")
    
    rtn_long = rtn_df.stack()
    print(type(rtn_long))
  
    return dataframe



df = create_dataframe()

df = load_all_data(df)

