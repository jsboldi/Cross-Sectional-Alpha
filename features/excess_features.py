import pandas as pd
import numpy as np
import yfinance as yf
import fastparquet
import matplotlib.pyplot as plt
import math

#calculate moving average 
def calculate_ma(filename,numdays):
    
    