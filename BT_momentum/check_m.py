from datetime import datetime 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


def momentum(closes):
    returns = np.log(closes)
    x = np.arange(len(returns))
    slope, _, rvalue, _, _ = linregress(x, returns)
    return ((1 + slope) ** 252) * (rvalue ** 2)  # annualize slope and multiply by R^2



if __name__ == '__main__':

    tickers = ['TSLA', 'AMC', 'GME', 'AAPL', 'MSFT', 'GOOG', 'AMZN']

    stocks = (
        (pd.concat(
            [pd.read_csv(f"./tickers/{ticker}.csv", index_col='Date', parse_dates=True)[
                'Close'
            ].rename(ticker)
            for ticker in tickers],
            axis=1,
            sort=True)
        )
    )
    stocks = stocks.loc[:,~stocks.columns.duplicated()]
    #print(stocks)

    momentums = stocks.copy(deep=True)
    for ticker in tickers:
        momentums[ticker] = stocks[ticker].rolling(90).apply(momentum, raw=False)
    #print(momentums)

    plt.figure(figsize=(12, 9))
    plt.xlabel('Days')
    plt.ylabel('Stock Price')

    bests = momentums.max().sort_values(ascending=False).index[:5]
    for best in bests:
        end = momentums[best].index.get_loc(momentums[best].idxmax())
        rets = np.log(stocks[best].iloc[end - 90 : end])
        x = np.arange(len(rets))
        slope, intercept, r_value, p_value, std_err = linregress(x, rets)
        plt.plot(np.arange(180), stocks[best][end-90:end+90])
        plt.plot(x, np.e ** (intercept + slope*x))

    plt.show()


