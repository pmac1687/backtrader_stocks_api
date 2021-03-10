from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
from stocks_data import ticker_data
from ticker import Ticker, query_data, get_indicators, plot_data
import csv

PREV_FRACTAL = []
PREV_FRACT_IND = []
FRACT = []
BUY_OBJS = []
BUY_PLOT = []
SELL = []
SELL_PLOT = []
SMA = []
TIME = []
WIN = 0
LOSE = 0

def simulate_backtest():
    global WIN
    global LOSE
    lose_arr = []
    win_arr = []
    #first signal for buy is fract_list;
    #takes 3 fracts for signal
    for a in range(len(t.fract)):
        if a > 1:
            good_fract = check_fract_range(a)
            if(good_fract):
                #for some reason AO array is one index short from the others
                #so this is bandaid
                if( a < 253):
                    buy = try_to_buy(a)



        else: continue
    compile_results()

def compile_results():
    global WIN
    global LOSE
    lose_arr = []
    win_arr = []
    for m in range(len(SELL)):
        if SELL[m]['cash_after'] > 10000:
            sell = SELL[m]['cash_after'] -10000
            WIN += sell
            win_arr.append(sell)
        else: 
            sell = 10000 - SELL[m]['cash_after']
            LOSE += sell
            lose_arr.append(sell)

    s = sum(win_arr) / len(win_arr)
    if len(lose_arr) == 0:
        p = 0
    else: p = sum(lose_arr) / len(lose_arr)
    for h in range(len(SELL)):
        print(SELL[h])
    print('win', s,'lose', p)
    #print(t.data.iloc[0].name)
    print_to_csv(s,p)
    print(t.data.index)
    print('win', WIN, 'loss', LOSE)
    print(SELL_PLOT)
    SMA[-1]= 0
    SMA[-2] = 0
    #SMA[-3] = 0
    #SMA[-4] = 0
    #SMA[-5] = 0
    #SMA[-6] = 0
    #SMA[-7] = 0
    #SMA[-8] = 0
    plt.figure()
    plt.plot(SELL_PLOT, 'o')
    plt.plot(SMA)
    plt.plot(FRACT, 'o')
    plt.plot(BUY_PLOT, 'ro')
    print('last', SMA[-4])
    print(BUY_PLOT)
    #plt.plot(TIME, SELL_PLOT, 'o')
    plt.show()

def print_to_csv(s,p):


    with open(f'{t.name}.csv', 'w', newline='') as file:
        fieldnames = ['stock', 'sell_p','cash_start','cash_after','position','AO_start','AO_sell','jaw','teeth', 'lips', 'ind','date_buy','date_sell']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for itm in SELL:
            writer.writerow({
                    'stock': itm['stock'],
                    'sell_p': itm['sell_p'],
                    'cash_start': itm['cash_start'],
                    'cash_after': itm['cash_after'],
                    'position': itm['position'],
                    'AO_start': itm['AO_start'],
                    'AO_sell': itm['AO_sell'],
                    'jaw': itm['jaw'],
                    'teeth': itm['teeth'],
                    'lips': itm['lips'],
                    'ind': itm['ind'],
                    'date_buy': itm['date_buy'],
                    'date_sell': itm['date_sell']
            })





def try_to_buy(a):
    prev_sma = PREV_FRACTAL[-1][1]
    #for b in range(a+1, len(t.fract)):
    b = a+1
    hit = False
    while hit == False:
        if b < 253:
            if t.sma[b] >= prev_sma:
                if (check_AO(b)) and (check_alligator(b)):
                    signal_buy(b)
                    signal_sell(b)
                    hit = True
                    break
                else: b+=1     
            else: b += 1
        else: hit = True

def signal_sell(b):
    #for c in range(b+1, len(t.fract)):
    if b < 250:
        c = b+1
        sale_p = t.fract[c][1]
        buy_p = t.fract[c-2] 
        pos = BUY_OBJS[-1]['position']
        profit = pos * sale_p
        for x in range(b+1, len(t.fract)):
            if t.fract[x][0] != '':
                sale_p = t.fract[x][1]
                buy_p = PREV_FRACTAL[-2][1] 
                pos = BUY_OBJS[-1]['position']
                win_loss = pos * sale_p
                sell_obj = {
                    'stock': t.name,
                    'sell_p': sale_p,
                    'cash_start': '$10,000',
                    'cash_after': win_loss,
                    'position': pos,
                    'AO_start': BUY_OBJS[-1]['AO'],
                    'AO_sell': t.AO[x],
                    'jaw': t.jaw[x],
                    'teeth': t.teeth[x],
                    'lips': t.lips[x],
                    'ind': c,
                    'date_buy': BUY_OBJS[-1]['date'],
                    'date_sell': t.data.iloc[x].name

                }
                SELL.append(sell_obj)
                SELL_PLOT[x] = int(sale_p)
                TIME[x] = str(t.data.iloc[c].name)
                break


    '''while hit == False:
        if t.fract[c] != '':
            if c< 253:
                sell_price = t.sma[c]
                pos = BUY_OBJS[-1]['position']
                win_loss = pos * sell_price
                sell_obj = {
                    'stock': t.name,
                    'sell_p': sell_price,
                    'cash_start': '$10,000',
                    'cash_after': win_loss,
                    'position': pos,
                    'AO_start': BUY_OBJS[-1]['AO'],
                    'AO_sell': t.AO[c],
                    'jaw': t.jaw[c],
                    'teeth': t.teeth[c],
                    'lips': t.lips[c],
                    'ind': c,
                    'date_buy': BUY_OBJS[-1]['date'],
                    'date_sell': t.data.iloc[c].name

                }
                SELL.append(sell_obj)
                SELL_PLOT[c] = int(sell_price)
                TIME[c] = str(t.data.iloc[c].name)
                hit = True
            else: hit = True
        else: c += 1'''
    '''#for c in range(b+1, len(t.fract)):
    hit = False
    c = b+1
    while hit == False:
        if t.fract[c] != '':
            if c< 253:
                sell_price = t.sma[c]
                pos = BUY_OBJS[-1]['position']
                win_loss = pos * sell_price
                sell_obj = {
                    'stock': t.name,
                    'sell_p': sell_price,
                    'cash_start': '$10,000',
                    'cash_after': win_loss,
                    'position': pos,
                    'AO_start': BUY_OBJS[-1]['AO'],
                    'AO_sell': t.AO[c],
                    'jaw': t.jaw[c],
                    'teeth': t.teeth[c],
                    'lips': t.lips[c],
                    'ind': c,
                    'date_buy': BUY_OBJS[-1]['date'],
                    'date_sell': t.data.iloc[c].name

                }
                SELL.append(sell_obj)
                SELL_PLOT[c] = int(sell_price)
                TIME[c] = str(t.data.iloc[c].name)
                hit = True
            else: hit = True
        else: c += 1'''

def signal_buy(b):
    buy_price = PREV_FRACTAL[-1][1]
    prev = PREV_FRACTAL[-1]
    cash = 10000
    position = cash/ buy_price
    buy_obj = {
        'stock_name': t.name,
        'buy_p': buy_price,
        'cash': cash,
        'position': position,
        'AO': t.AO[b],
        'jaw': t.jaw[b],
        'teeth': t.teeth[b],
        'lips': t.lips[b],
        'ind': b,
        'prev_fract': prev,
        'prev_fract_ind' : PREV_FRACTAL[-1][2],
        'date': t.data.iloc[b].name
    }
    BUY_PLOT[PREV_FRACTAL[-1][2]] = buy_price
    BUY_OBJS.append(buy_obj)

def check_alligator(a):
    if a < 253:
        if t.sma[a] > t.jaw[a] and t.sma[a] > t.teeth[a] and t.sma[a] > t.lips[a]:
            return True
        else: return False
    else: return False

def check_AO(a):
    if(a<253):
        if t.AO[a] > 0:
            return True
        else: return False
    else: return False

def check_fract_range(a):
    if len(PREV_FRACTAL) > 2:
        current = t.fract[a]
        last = PREV_FRACTAL[-1]
        bef_last = PREV_FRACTAL[-2]
        if current[0] == '':
            return False
        if current[0] == 'down' and last[0] == 'up' and bef_last[0] == 'down':
            PREV_FRACTAL.append(t.fract[a])
            return True
        else: 
            PREV_FRACTAL.append(t.fract[a])
            return False
    else:
        PREV_FRACTAL.append(t.fract[a])
        return False





if __name__ == '__main__':
    df = query_data()
    df = get_indicators(df)
    t = Ticker('aapl',df)
    for k in range(len(t.sma)):
        SELL_PLOT.append(0)
        BUY_PLOT.append(0)
        TIME.append(0)
        if t.fract[k] != '':
            FRACT.append(int(t.sma[k]))
        else: FRACT.append(0)
        SMA.append(int(t.sma[k]))
    simulate_backtest()
    print(t.fract_high[0])