import Ticker
import math
import matplotlib.pyplot as plt

# basic ao. first check is AO is below zero
# second is fractal low peak is more the prev fractal low peak
# Ao increases toward 0
# crosses zero, buy
# ? exit, 2 consecutive less AO bars?
WINS=[]
def check_ao_negative(ao, below_zero):
    if ao < 0:
        return True
    else:
        return False

def check_swing_low(AO, i):
    ao = AO[i]
    if (ao > AO[i-1]) and  (AO[i-1] > AO[i-2]) and (AO[i-2] < AO[i-3]) and (AO[i-3] < AO[i-4]) :
        ind = i-2
        ao = AO[i-2]
        return ind
    else:
        return 0

def signal_sell(b,i,ticker,ind,position,high,high_ind):
        sell_p = (ticker.data['High'][b] + ticker.data['Low'][b])/2
        sold = position * sell_p
        print('sold', sold)
        print('sp', sell_p)
        buy_p = (ticker.data['High'][i] + ticker.data['Low'][i])/2
        print({'buy': buy_p, 'sell': sell_p, 'w-l': sold, 'buys': i, 'selle': b, 'high':high, 'high_ind': high_ind})
        WINS.append(sold)


def look_to_sell(position,i,  ticker, ind):
    bought = ticker.data['ao'][i]
    last = 0
    before_last = 0
    high = 0
    high_ind = 0
    for b in range(i, len(ticker.data['ao'])):
        ao = ticker.data['ao']
        med = (ticker.data['High'][b] + ticker.data['Low'][b])/2
        if high < med:
            high = med
            high_ind = b
        if ao[b] < 0:
            signal_sell(b,i,ticker,ind,position, high, high_ind)
            break






def buy(i, AO, ticker, ind):
    cash = 100000
    price = (ticker.data['High'][i] + ticker.data['Low'][i]) /2
    print(price)
    position = cash/price
    print('pos', position)
    look_to_sell(position,i, ticker, ind)


def look_to_buy(AO, ind, ticker):
    print('signal', AO[ind])
    for i in range(ind, len(ticker.data['ao'])):
        ao = ticker.data['ao'][i]
        if ao >= 0:
            print('cross',ao)
            print('high', ticker.data['High'][i])
            print('low', ticker.data['Low'][i])

            buy(i,AO, ticker, ind)
            break



def run_test(ticker):
    prev_low = 0
    prev_swing_low = 0
    prev_low_ind = 0
    swing_low = 0
    ind = 0
    below_zero = False
    AO = ticker.data['ao']
    for i in range(len(AO)):
        ao = AO[i]
        if (math.isnan(ao))==False:
            below_zero = check_ao_negative(ao, below_zero)
            if (below_zero):
                if i >= 4:
                    ind = check_swing_low(AO, i)
                    if ind != 0:
                        swing_low = AO[ind]
                        print(swing_low)
                        if prev_low_ind != 0:
                            if prev_low < swing_low:
                                look_to_buy(AO, ind, ticker)
                                prev_low == swing_low
                                


        if swing_low != 0:
            prev_low = swing_low
            prev_low_ind = ind
        swing_low = 0
        ind = 0
            

if __name__=='__main__':
    ticker = Ticker.Ticker('baba')
    run_test(ticker)
    