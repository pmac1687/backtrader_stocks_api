import pandas as pd
import quandl as q
import matplotlib.pyplot as plt
import numpy as np

"""
SMAC strategy
3 m_avg lookback periods
short,mid,long
buy signal when short moves above long
sell signal when short dips back below long
"""

q.ApiConfig.api_key = 'Ms91AzsAsj7GyZx25Ns6'

msft_data = q.get("EOD/MSFT", start_date="2010-01-01", end_date="2019-01-01")

short_lb = 50
long_lb = 120

#new dataframe with signal column
signal_df = pd.DataFrame(index=msft_data.index)
signal_df['signal'] = 0.0

# step3: create a short simple moving average over the short lookback period
signal_df['short_mav'] = msft_data['Adj_Close'].rolling(window=short_lb,min_periods=1, center=False).mean()
#%%

# step4: create long simple moving average over the long lookback period
signal_df['long_mav'] = msft_data['Adj_Close'].rolling(window=long_lb, min_periods=1, center=False).mean()

# step5: generate the signals based on the conditional statement
signal_df['signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)   

# step6: create the trading orders based on the positions column
signal_df['positions'] = signal_df['signal'].diff()

print(signal_df['positions'])


# initialize the plot using plt
fig = plt.figure()

# Add a subplot and label for y-axis

plt1 = fig.add_subplot(111,  ylabel='Price in $')

msft_data['Adj_Close'].plot(ax=plt1, color='r', lw=2.)

# plot the short and long lookback moving averages
signal_df[['short_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))

# plotting the sell signals

plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, signal_df.short_mav[signal_df.positions == -1.0],'v',markersize=10, color='k')

# plotting the buy signals

plt1.plot(signal_df.loc[signal_df.positions == 1.0].index, signal_df.short_mav[signal_df.positions == 1.0],'^', markersize=10, color='m')         # Show the plotplt.show()

plt.show()