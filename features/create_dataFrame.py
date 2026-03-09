import volatility
import momentum
import pandas as pd
import numpy as np
import sklearn
import lightgbm as lgb





def create_dataframe():
    dataframe = pd.DataFrame(columns=["Date","Ticker","5dayReturn","63dayMomentum","20dayVolatility","Forward 5dreturn"])
    
    return dataframe


def load_all_data():
    rtn_df = pd.read_parquet("../data/return5day.parquet",engine = "pyarrow")
    vol_df = pd.read_parquet("../data/volatility.parquet", engine = "pyarrow")
    mom_df = pd.read_parquet("../data/21daymomentum.parquet",engine = "pyarrow")
    
    print(rtn_df.loc[:,'Ticker'])
    
    
    print(mom_df)
    
    rtn_long = rtn_df.stack().rename("ret_1d")
    vol_long = vol_df.stack().rename("20day_vol")
    mom_long = mom_df.stack().rename("mom_63d")
    
    #5 day forward log return
    forward_5d = np.log(rtn_df.shift(5)/rtn_df)
    
    forward_5d_long = forward_5d.stack().rename("forward 5d rtn")
    
    print(type(rtn_long))
    
    df = pd.concat([rtn_long,vol_long,mom_long,forward_5d_long],axis = 1,verify_integrity= 1).reset_index()
    
    
    return df







df = load_all_data()

df.to_parquet()


print(df)

print(df.iloc[29377])

print(df.iloc[31877])

