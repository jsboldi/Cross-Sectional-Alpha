import pandas as pd
import numpy as np
import yfinance as yf
import bs4


def find_tickers():
    with open("rawHTML.html",'r',encoding = "utf-8") as file:
        base_html = file.read()
        tickerlist = []
        soup = bs4.BeautifulSoup(base_html,features = "html.parser")
        for tag in soup.find_all(class_ = "external text"):
            if (len(tag.text) <= 4):
                tickerlist.append(tag.text)
                
    return tickerlist
            
            
def print_tickers(tickerList):
    for ticker in tickerList:
        print(ticker)
        




def  load_price_history(tickerList):
    data = yf.download(tickerList,'2023-01-01','2025-12-31')
    print(data['Close'].iloc[0])
    return 
    
    

    
    

    
