from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta

#array: [open, high, low, close, volume]

class ticker_data():
    def __init__(self, ticker, date_range='null'):
        self.name = ticker.upper()
        # format date_range : ["2018-01-01", "2019-01-01"]
        self.date_range = date_range
        #self.period = period
        self.data_np, self.data_pd = self.get_ticker_data()
        self.highs, self.lows, self.open, self.close, self.volume = self.get_constants_from_data()
        self.dates = self.get_dates()
        self.med_price = self.get_med_price()
        self.sma5 = self.get_slow_moving_average(p=5)
        #self.sma5 = self.get_awesome_ossilator(p=5)
        self.sma34 = self.get_slow_moving_average(p=34)
        self.AO = self.get_awesome_oss()
        self.jaw = self.calculate_alligator(13,8)#522
        self.teeth = self.calculate_alligator(8,5)#519 perfect
        self.lips = self.calculate_alligator(5,3)#517

    def calculate_alligator(self,N, start):
        #### broke but on the right track
        # if start 8, shift array 8 left and last 8=0 and start iter
        #med price has 1525, shift 8 group 13
        #start at 13+8=23 to grab all
        arr = []
        length = len(self.med_price)
        med = self.med_price
        begin = N 
        #smma = sum(self.med_price[length - N:]) / N
        #arr.append(smma)
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

    def get_awesome_oss(self):
        print(len(self.med_price))
        #len med prices = 1525
        ao = []
        length = len(self.sma34)
        for i in reversed(range(length)):
            sma_diff = self.sma5[i] - self.sma34[i]
            ao.append(sma_diff)
        return ao[::-1]

    def get_slow_moving_average(self, p):
        sma_arrs = []
        #reverse to capture newest date back 1525-0; 1525-30
        length = len(self.med_price)
        for i in reversed(range(p, length)):
            period_arr = self.med_price[i-p:i]
            sma = sum(period_arr)/p
            sma_arrs.append(sma)
        missing = length 
        while len(sma_arrs) < missing:
            sma_arrs.append(0)
        return sma_arrs[::-1]
        



        '''for i in reversed(range(self.period)):#reverse range of 90
            sma_arr = []
            #start 90, so need 89,88,
            for b in range(i, self.period - p ):
                sma_arr.append(self.med_price[b])
                if len(sma_arr) == p:
                    sma = sum(sma_arr) / p
                    arr.append(sma)
                    sma_arr = []
                    print('sma',sma)
        return arr'''




    def get_med_price(self):
        med_prices = []
        for i in range(len(self.lows)):
            med = (self.highs[i] + self.lows[i]) /2
            print('med_price', med)
            med_prices.append(med)
        return med_prices

    def get_ticker_data(self):
        if(self.name):
            today = date.today() 
            yesterday = today - timedelta(days = 1) 
            try:
                pd_data = get_stock_data(self.name, "2017-01-01", yesterday)
                np_data = pd_data.values
            except Exception as e:
                print('get stock data error, query misformed line 20')
                print(e)
            return np_data, pd_data

    def get_constants_from_data(self):
        opens = []
        close = []
        high = []
        low = []
        volume = []
        data = self.data_np
        for i in range(len(data)):
            opens.append(data[i][0])
            high.append(data[i][1])
            low.append(data[i][2])
            close.append(data[i][3])
            volume.append(data[i][4])
        return high, low, opens, close, volume

    def get_dates(self):
        data = self.data_pd
        dates = []
        for i in range(len(data.index)):
            dates.append(data.iloc[i].name)
        return dates

        


if __name__ == '__main__':
    ticker = ticker_data('tsla')
    '''plt.bar(range(90), ticker.AO)
    plt.plot(range(90), ticker.sma5)
    plt.plot(range(90), ticker.sma34)
    plt.plot(range(90), ticker.med_price[len(ticker.med_price)-90:] )
    plt.show()
    plt.plot(range(90), ticker.close[len(ticker.close)-90:] )
    plt.plot(range(90), ticker.open[len(ticker.open)-90:] )
    plt.plot(range(90), ticker.highs[len(ticker.highs)-90:] )
    plt.plot(range(90), ticker.lows[len(ticker.lows)-90:] )
    plt.show()
    plt.plot(range(90), ticker.volume[len(ticker.volume)-90:] )
    plt.show()'''
    print('len', len(ticker.med_price))
    plt.plot(ticker.sma34)
    plt.plot(ticker.sma5)
    plt.bar(range(len(ticker.AO)),ticker.AO)
    plt.show()
    plt.plot(ticker.jaw)
    plt.plot(ticker.teeth)
    plt.plot(ticker.lips)
    plt.show()