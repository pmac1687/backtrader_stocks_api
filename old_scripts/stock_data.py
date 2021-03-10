from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta

class ticker_data():
    def __init__(self, ticker, date_range='null', period='null'):
        self.name = ticker.upper()
        # format date_range : ["2018-01-01", "2019-01-01"]
        self.date_range = date_range
        self.period = period
        self.dates, self.data, self.all_dates = self.get_ticker_data()
        self.highs = self.get_highs()
        self.lows = self.get_lows()
        self.med_price = self.get_med_price()
    
    def get_awesome_ossilator(self, p=5):
        #sma= small moving avg., = sum(med_price for 5days)/5
        sma = []
        for i in range(len(self.med_price)):
            med_lst = []
            date = self.dates[i]
            print('date', date)
            b = i
            day = 0
            while len(med_lst) != p:
                if b == i:
                    med_lst.append(date)
                    b -= 1
                else:
                    dat = med_lst[-1]
                    if day == 0:
                        day = int(dat.date().day)
                        day -= 1
                    if day != 1:
                        month = int(dat.date().month)
                        year = int(dat.date().year)
                        day -= 1
                        poss_date = pd.Timestamp(f'{year}-{month}-{day}')
                        print(poss_date)
                        print(self.dates[0])
                        if (self.data.info):
                            med_lst.append(poss_date)
                        print(med_lst)
                            

            all_dates_index = self.data.loc[date]
            print('date',date.year)
            
            
            
            '''for b in range(i, i + period):
                date = self.dates[b]
                high = self.data_extra.loc[date].high
                low = self.data_extra.loc[date].low
                avg = (high + low) / 2
                med_lst.append(avg)
                if len(med_lst) == period:
                    res = sum(med_lst) / period
                    sma.append(res)
                    lst = []'''
        return sma

    
    def get_med_price(self):
        med_price = []
        for i in range(len(self.lows)):
            med = (self.highs[i] + self.lows[i]) / 2
            med_price.append(med)
        return med_price


    def get_lows(self):
        lows = []
        for i in range(self.period):
            date = self.dates[i]
            low = self.data.loc[date].low
            lows.append(low)
        return lows

    def get_highs(self):
        highs = []
        for i in range(self.period):        
            date = self.dates[i]
            high = self.data.loc[date].high
            highs.append(high)
        return highs

    def get_ticker_data(self):
        if(self.period):
            today = date.today() 
            yesterday = today - timedelta(days = 1) 
            try:
                arr_data = get_stock_data("TSLA", "2015-01-01", yesterday)
                print(arr_data)
            except Exception as e:
                print('get stock data error, query misformed line 20')
                print(e)
            dates = []
            print(arr_data.iloc)
            for i in reversed(range(len(arr_data.index))):
                print(1)
                dates.append(arr_data.iloc[i].name)
                if len(dates) == self.period:
                    break
            result = []
            for b in reversed(dates):
                result.append(b)
            all_dates = []
            for c in range(len(arr_data.index)):
                all_dates.append(arr_data.iloc[c].name)

            return result, arr_data, all_dates


if __name__ == '__main__':
    ticker = ticker_data('me',period=90)
    ticker.get_awesome_ossilator(5)