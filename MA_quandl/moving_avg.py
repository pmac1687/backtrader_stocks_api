import pandas as pd
import quandl as q
import matplotlib.pyplot as plt
import numpy as np

q.ApiConfig.api_key = 'Ms91AzsAsj7GyZx25Ns6'

msft_data = q.get("EOD/MSFT", start_date="2010-01-01", end_date="2019-01-01")

adj_price = msft_data['Adj_Close']

mav = adj_price.rolling(window=50).mean()

mav.plot()

plt.show()

#print(msft_data.head())