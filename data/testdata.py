import load_data
from load_data import load_price_history
from load_data import find_tickers
from load_data import print_tickers

import yfinance as yf
import scrape_data


tickers = find_tickers()

load_price_history(tickers)