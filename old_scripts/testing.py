from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta
from stocks_data import ticker_data

#  obj = { 'ind_history': i, 'ind_fract': len(fractal_hits) +1, 'bound': 'lower', 'prev': state, 'med_price': t.med_price[i], 'ao': t.AO[i],'close': t.close[i], 'high': t.highs[i], 'low': t.lows[i]}
fractal_hits = []
fractal_inds = []
TREND = 'none'
buy_cond = []
sell_cond = []
CASH = 10000
wins_arr = []

def run_history():
    period = len(t.med_price)
    for i in range(period):
        if i >= 2 and i <= period -3:
            get_fractal(i)

            '''if ao == 'true':
                gtg = check_prev_fract(i)
            else: gtg = 'false'
            if gtg == 'true':
                simulate_buy_period(i)'''

def simulate_backtest():
    for a in range(len(fractal_hits)):
        curr_fract = fractal_hits[a]
        g2g =  check_prev_fract(a)
        if g2g == 'false':
            print('hit false')
            continue
        if g2g == 'true':
            print('hit buy')
            buy(a)
            sell(a)
            continue

def sell(a):
    get_nxt = 'true'
    current_t = fractal_hits[a]['trend']
    b = a + 1
    if( a+1 <= len(fractal_hits) - 2):
        while get_nxt == 'true':
            if( b <= len(fractal_hits) - 2):
                b+=1
                nxt_fract = fractal_hits[b]
                nxt_fract_t = nxt_fract['trend']
                if current_t != nxt_fract_t:
                    print('$$$$$$$$$$')
                    nxt_fract_sell_price = nxt_fract['close']
                    stock_len = buy_cond[-1]['stock_len']
                    winning = nxt_fract_sell_price * stock_len
                    buy_ind = buy_cond[-1]['hist_ind']
                    sell_ind = nxt_fract['ind_history']
                    sell = {'sell_price': nxt_fract_sell_price,'buy_price': 10000/stock_len, 'stock_len': stock_len, 'win/loss': winning, 'start': 10000, 'buy_ind': buy_ind, 'sell_ind': sell_ind }
                    sell_cond.append(sell)
                    print('sell', sell)
                    get_nxt = 'false'


            else: 
                get_nxt = 'false'
                sell_cond.append(0)



def buy(a):
    cash = 10000
    current = fractal_hits[a]
    prev = fractal_hits[a-1]
    ind = current['ind_history']
    for b in range(ind+1, len(t.med_price)):
        if t.med_price[b] >= prev['med_price']:
            stocks = cash / t.close[b]
            buy = {'stock_len': stocks, 'buy_price': t.close[b], 'hist_ind': b, 'fract_ind': a, 'next_fract_ind': a+1}
            buy_cond.append(buy)
    print(buy_cond[0])


def simulate_buy_period(i):
    global TREND
    current = fractal_hits[-1]
    last = fractal_hits[-2]
    bef_last = fractal_hits[-3]
    buy_med = last['price']
    for b in  range(i, len(t.med_price)):
        if b != i:
            #print('hit')
            #print(t.med_price[b], buy_price)
            if TREND == 'up':
                next_med = t.med_price[b]
                print(next_med,buy_med)
                if next_med >= buy_med:
                    print('hitsfkhgfkhgfkhg')
                    cond = [i, b, buy_med, TREND]
                    TREND = 'none'
                    buy_cond.append(cond)
                    trigger_buy(i,b)
                    break

            if TREND == 'down':
                next_med = t.med_price[b]
                if next_med <= buy_med:
                    cond = [i, b, buy_med, TREND]
                    TREND = 'none'
                    buy_cond.append(cond)
                    trigger_buy(i,b)
                    break
            if TREND == 'none':
                break
    print(sell_cond)

def trigger_buy(i, b):
    print('trigger')
    global buy_cond
    global CASH
    global wins_arr
    global sell_cond
    #cond= ind of cond , ind of buy trigger, med_price, TREND
    cond = buy_cond[-1]
    buy_price = t.close[b]
    trend = cond[3]
    stock_len = CASH / buy_price
    #grab next fractal, get day index, get price cash out
    for d in range(len(fractal_inds)):
        print(fractal_inds[d], b)
        if fractal_inds[d] > b:
            print('trigger 2')
            sell_fract = fractal_hits[d]
            price_ind = sell_fract['ind']
            sell_price = t.close[price_ind]
            tot_cash = sell_price * stock_len
            wins_arr.append(tot_cash)
            cond = [price_ind, buy_price, sell_price, d ,tot_cash , trend]
    
    
            
def check_prev_fract(a):
    global TREND
    if  a < 2:
        return 'false'
    current = fractal_hits[a]
    last = fractal_hits[a-1]
    bef_last = fractal_hits[a-2]
    #print('###########',current)
    if current['trend'] == 'up' and last['trend'] == 'down' and bef_last['trend'] == 'up':
        if current['ao'] > bef_last['ao']:
            TREND = 'down'
            return 'true'
    if current['trend'] == 'down' and last['trend'] == 'up' and bef_last['trend'] == 'down':
        if current['ao'] > bef_last['ao']:
            TREND = 'up'
            return 'true'
    print('missed')
    return 'false'

def get_fractal(i):
    ao = t.AO
    current = ao[i]
    #upper fractal
    if len(t.AO) -3 >= i >= 2:
        last = ao[i-1]
        bef_last = ao[i-2]
        nxt = ao[i+1]
        nxt_aft = ao[i+2]
        prev_higher = 'true' if current < last < bef_last else 'false'
        prev_lower = 'true' if (current > last) and (last > bef_last) else 'false'
        aft_higher = 'true' if current < nxt < nxt_aft else 'false'
        aft_lower = 'true' if current > nxt > nxt_aft else 'false'
        print('current',bef_last, last,  current, nxt, nxt_aft)
        #upper fractal, trending down
        if (prev_lower=='true' and aft_lower=='true'):
            state = fractal_hits[-1]['med_price'] if len(fractal_hits) > 0 else 'null'
            fractal_inds.append(i)
            obj = { 'ind_history': i, 'ind_fract': len(fractal_hits) , 'trend': 'down', 'prev_fract_med': state, 'med_price': t.med_price[i], 'ao': t.AO[i],'close': t.close[i], 'high': t.highs[i], 'low': t.lows[i]}
            fractal_hits.append(obj)
            return 'true'
        #lower fractal, trending up
        if (prev_higher=='true' and aft_higher=='true'):
            state = fractal_hits[-1]['med_price'] if len(fractal_hits) > 0 else 'null'
            fractal_inds.append(i)
            obj = { 'ind_history': i, 'ind_fract': len(fractal_hits) , 'trend': 'up', 'prev_fract_med': state, 'med_price': t.med_price[i], 'ao': t.AO[i],'close': t.close[i], 'high': t.highs[i], 'low': t.lows[i]}
            fractal_hits.append(obj)
            return 'true'

    
    return 'false'

if __name__ == '__main__':
    t = ticker_data('gme')
    print('len', len(t.jaw))
    print(t.jaw)
    plt.bar(range(len(t.med_price)),t.AO)
    #plt.plot(t.teeth)
    #plt.plot(t.lips)
    #plt.plot(t.med_price)
    plt.show()
    run_history()
    simulate_backtest()
    print('len',len(fractal_hits))
