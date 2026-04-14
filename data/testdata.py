import fastparquet.dataframe
import load_data
from load_data import load_price_history
from load_data import find_tickers
from load_data import print_tickers
import yfinance as yf
import scrape_data
import fastparquet
import pandas as pd


tickers = find_tickers()


dataframe = pd.DataFrame(load_price_history(tickers))

dataframe = dataframe.astype(dtype='float32')


dataframe.to_parquet('data.parquet', engine = 'pyarrow',compression= 'snappy')
