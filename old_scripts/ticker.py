from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
from tapy import Indicators

from datetime import datetime

class Ticker():
    def __init__(self,name,df):
        self.name = name
        self.data = df
        self.AO = df['AO']
        self.sma = df['sma']
        self.high = df['High']
        self.low = df['Low']
        self.fract_high = df['fractal_highs']
        self.fract_low = df['fractal_lows']
        self.jaw = self.calculate_alligator(13,8)#522
        self.teeth = self.calculate_alligator(8,5)#519 perfect
        self.lips = self.calculate_alligator(5,3)#517
        self.fract_coords = self.get_fract_coords()
        self.fract = self.get_fract_ind_arr()



    def get_fract_ind_arr(self):
        arr = []
        #up or down refers to if is high or low fract for graph purpose
        #if '' empty no fract for that index
        #sma will be used later in backtesting to indicate 'price' for our purpose,
        #as prev fract sma indicates buy and next fract sma = sell indicator
        for i in range(len(self.fract_high)):
            if (self.fract_high[i]) == True:
                arr.append(['up', self.sma[i], i])
            if (self.fract_low[i]) == True:
                arr.append(['down',self.sma[i], i])
            else: arr.append(['',self.sma[i]])
            


        print(arr)
        return arr


    def calculate_alligator(self,N, start):
        # if start 8, shift array 8 left and last 8=0 and start iter
        #med price has 1525, shift 8 group 13
        #start at 13+8=23 to grab all
        arr = []
        length = len(self.sma)
        for b in range(len(self.sma)):
            try:
                int(self.sma[b])
            except ValueError:
                print(self.sma[b])
                self.sma[b] = 0
                print(self.sma[b])
        med = self.sma
        begin = N 
        #smma = sum(self.med_price[length - N:]) / N
        #arr.append(smma)
        print('med',med[0])
        for i in range(begin, length):
            if i == begin:
                smma = sum(med[i-N:i]) / N
                arr.append(smma)
            if i != begin:
                prev_sum = arr[-1] * N
                sma = sum(med[i - N:i]) / N
                smma = ( prev_sum - arr[-1] + sma) / N
                arr.append(smma)
        # they all have diff sma periods, 13,8, 5 being smallest and limit, prepend N zeroes
        print('pre',len(arr))
        diff = N - start
        for b in range(diff):
            arr.insert(0,0)
        for f in range(start):
            arr.append(0)
        return arr

    def get_fract_coords(self):
        arr = []
        df = pd.DataFrame()
        #df.columns = ['date', 'coord']
        for i in range(len(self.fract_high)):
            print(i)
            if (self.fract_high[i]):
                coord = [i, self.high[i]]
                #df.insert(i,'date', self.data.iloc[i].name, 'coord',self.high[i])
                #df.insert(i,'coord', self.high[id])
                arr.append(coord)
            if (self.fract_low[i]):
                coord = [i, self.low[i]]
                #df.insert(i,'date', self.data.iloc[i].name)
                #df.insert(i,'coord', self.high[id])
                arr.append(coord)
        
        return df

def plot_data(t):
    #plt.plot(t.sma)
    #plt.plot(t.jaw)
    #plt.plot(t.teeth)
    #plt.plot(t.lips)
    plt.show()

def query_data():
    return get_stock_data('baba', "2020-01-28", "2021-01-28")

def get_indicators(df):
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', ]
    df.rename(index={'dt': 'Datetime'})
    indicators = Indicators(df)
    indicators.awesome_oscillator(column_name='AO')
    #indicators.smma()
    #indicators.alligator()
    indicators.sma(column_name='sma')
    indicators.fractals(column_name_high='fractal_highs', column_name_low='fractal_lows')
    df = indicators.df
    
    return df


if __name__ == '__main__':
    df = query_data()
    df = get_indicators(df)
    t = Ticker('tsla',df)
    plot_data()
    print(t.AO[0])

    