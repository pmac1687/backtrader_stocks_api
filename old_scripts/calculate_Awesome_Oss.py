from fastquant import get_stock_data, backtest
import matplotlib.pyplot as plt
import numpy as np

tsla = get_stock_data("TSLA", "2018-01-01", "2019-01-01")
# .iloc[index] returns you index obeject complete frame 'iloc'
# .index[index] returns date or 'index' of frame
# .loc['volume', 'close'] ranges of columns
# .attrs returns dict keys
print(tsla.iloc[0].high)
HIGHS = []
LOWS = []
MED_PRICE = []
FIVE_DAY = []
THIRTY_FOUR_DAY = []
AO = []
INDEX = []

def get_high_low():
    for i in range(len(tsla)):
        HIGHS.append([tsla.iloc[i].name,tsla.iloc[i].high])
        LOWS.append([tsla.iloc[i].name, tsla.iloc[i].low])

def get_med_price():
    for i in range(len(HIGHS)):
        MED_PRICE.append([HIGHS[i][0], [(HIGHS[i][1] + LOWS[i][1])/2]])
        print(MED_PRICE)

def plot_data():
    highs = np.array(HIGHS)
    lows = np.array(LOWS)
    med_p = np.array(MED_PRICE)
    plt.plot(highs, 'o', color='g')
    plt.plot(lows, 'o', color='r')
    plt.plot(med_p, color='b')
    plt.show()

def get_awesome_oss():
    #AO= SMA(med_pri/5days) - SMA(med_price/34days)
    #SMA = sum(med_price, N)/ N
    #were doing 90 days back
    med = MED_PRICE
    print(med[0][1][0])
    for a in range(1, 91):
        #five day SMA, array reversed to start from
        #most recent date back
        sma = (med[-(a)][1][0] + med[-(a+1)][1][0] + med[-(a+2)][1][0] + med[-(a+3)][1][0] + med[-(a+4)][1][0]) / 5
        print(sma)
        FIVE_DAY.append([med[-a][0],sma])
        print(sma)
        sma34 = []
        #34 day SMA, array revesed
        for b in range(a, a + 34):
            sma34.append(med[-b][1][0])
            if(len(sma34) == 34):
                sma34 = sum(sma34) / 34
                THIRTY_FOUR_DAY.append([med[-b][0], sma34])
                sma34 = []
    for c in reversed(range(len(FIVE_DAY))):
        print(THIRTY_FOUR_DAY)
        print(FIVE_DAY[c])
        ao = FIVE_DAY[c][1] - THIRTY_FOUR_DAY[c][1]
        INDEX.append(c)
        AO.append(ao)
    plt.bar(INDEX,AO)
    #highs = np.array(HIGHS[1])
    #lows = np.array(LOWS[1])
    #med_p = np.array(MED_PRICE[1])
    plt.plot(HIGHS[1], 'o', color='g')
    plt.plot(LOWS[1], 'o', color='r')
    plt.plot(MED_PRICE[1], color='b')
    plt.show()
    print(AO)

        




if __name__ == '__main__':
    get_high_low()
    get_med_price()
    get_awesome_oss()
    plot_data()