from pandas_datareader import data as pdr
from datetime import datetime
import pandas as pd

start = datetime(2012,5,31)
end = datetime(2018,3,1)

stocks = ['TSLA', 'AMC', 'GME', 'AAPL', 'MSFT', 'GOOG', 'AMZN']

for stock in stocks:
    
    f = pdr.get_data_yahoo(stock, start=start, end=end)

    f.to_csv(f'./tickers/{stock}.csv')