import pandas as pd
import numpy as np
import requests
import bs4
import os

headers = {
    "User-Agent": (
        "Academic research project for cross-sectional  equity modeling"
        "(contact: jsboldi@clemson.edu)"
    )
}


# i am using the wikipedia page with the s&p 500 table to actually get the tickers of the currently listed companies

download_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

res = requests.get(download_url, headers= headers)
soup = bs4.BeautifulSoup(res.text, features = 'html.parser')

with open('rawHTML.html','w', encoding = 'utf-8') as file:
    file.write(res.text)


