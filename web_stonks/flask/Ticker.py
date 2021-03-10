from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
from tapy import Indicators
from pandas_datareader import data as pdr


from datetime import datetime

class Ticker():
    def __init__(self,name):
        self.name = name
        today = date.today().strftime("%Y-%m-%-d").split('-')
        day, month, year = [today[2],today[1], today[0]]
        end = datetime(int(year),int(month),int(day))
        start = datetime(2015, 9, 7 )
        self.data = pdr.get_data_yahoo(self.name, start=start, end=end)
        self.data = self.get_indicators(self.data)



    def get_indicators(self, df):
        print(df.index)

        #df.index.name = 'Datetime'
        indicators = Indicators(df)
        indicators.awesome_oscillator(column_name='ao')
        indicators.accelerator_oscillator(column_name='ac')
        indicators.accumulation_distribution(column_name='a/d')
        indicators.atr(period=14, column_name='atr')
        indicators.bears_power(period=13, column_name='bears_power')
        indicators.bulls_power(period=13, column_name='bulls_power')
        indicators.cci(period=14, column_name='cci')
        indicators.de_marker(period=14, column_name='dem')
        indicators.ema(period=5, column_name='ema', apply_to='Close')
        indicators.force_index(period=13, method='sma', apply_to='Close', column_name='frc')
        indicators.ichimoku_kinko_hyo(period_tenkan_sen=9, period_kijun_sen=26, period_senkou_span_b=52, column_name_chikou_span='chikou_span', column_name_tenkan_sen='tenkan_sen', column_name_kijun_sen='kijun_sen', column_name_senkou_span_a='senkou_span_a', column_name_senkou_span_b='senkou_span_b')
        indicators.bw_mfi(column_name='bw_mfi')
        indicators.momentum(period=14, column_name='momentum')
        indicators.mfi(period=5, column_name='mfi')
        indicators.macd(period_fast=12, period_slow=26, period_signal=9, column_name_value='macd_value', column_name_signal='macd_signal')
        indicators.bollinger_bands(period=20, deviation=2, column_name_top='bollinger_up', column_name_mid='bollinger_mid', column_name_bottom='bollinger_bottom')
        #indicators.smma(period=5, column_name='smma', apply_to='Close')
        #indicators.gator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_val1='value1', column_name_val2='value2')
        #indicators.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='alligator_jaw', column_name_teeth='alligator_teeth', column_name_lips='alligator_lips')
        #indicators.smma(period=5, column_name='smma', apply_to='Close')
        indicators.sma(column_name='sma')
        indicators.fractals(column_name_high='fractal_highs', column_name_low='fractal_lows')
        df = indicators.df

        return df


if __name__=='__main__':
    tick = Ticker('baba')
    print(tick.data['momentum'])