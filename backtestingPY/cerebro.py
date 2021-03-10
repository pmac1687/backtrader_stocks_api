# -*- coding: utf-8 -*-

import backtrader as bt
from datetime import date

class PrintClose(bt.Strategy):

    def __init__(self):
        #Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        
    def log(self, txt, dt=None):
        date = self.datas[0].datetime.date(0)
        print(f'{date} {txt} {dt}')
        
        
    

    def next(self):
        self.log('Close: ', self.dataclose[0])
        
if __name__=="__main__":
    #Instantiate Cerebro engine
    cerebro = bt.Cerebro()

    #Add data feed to Cerebro
    data = bt.feeds.YahooFinanceCSVData(dataname='../AAPL.csv')
    cerebro.adddata(data)

    #Add strategy to Cerebro
    cerebro.addstrategy(PrintClose)

    #Run Cerebro Engine
    cerebro.run()