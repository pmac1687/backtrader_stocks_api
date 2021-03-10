from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
from tapy import Indicators

arr = []

df = get_stock_data('tsla', "2017-01-01", "2020-01-01")
print(df.columns)
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
indicators = Indicators(df)
indicators.awesome_oscillator(column_name='AO')
indicators.sma(column_name='sma')
# Indicators.fractals(column_name_high='fractals_high', column_name_low='fractals_low')
indicators.fractals(column_name_high='fractal_highs', column_name_low='fractal_lows')
df = indicators.df
print(df.tail())
plt.plot(df['sma'])
plt.plot(df['AO'])
plt.plot(df['fractal_highs'])
plt.plot(df['fractal_lows'])
plt.show()