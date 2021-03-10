# importing the flask library files
from flask import Flask
import Ticker
import json
from flask_cors import CORS

#create flask web app object
app = Flask(__name__)
CORS(app)

# define http route
@app.route("/<stock>")
def index(stock):
    print(stock)
    tic = Ticker.Ticker(stock)
    date = tic.data.index
    _open = tic.data['Open']
    close = tic.data['Close']
    high = tic.data['High']
    low = tic.data['Low']
    volume = tic.data['Volume']
    ao = tic.data['ao']
    ac = tic.data['ac']
    ad = tic.data['a/d']
    atr = tic.data['atr']
    bep = tic.data['bears_power']
    bup = tic.data['bulls_power']
    cci = tic.data['cci']
    dem = tic.data['dem']
    ema = tic.data['ema']
    frc = tic.data['frc']
    cncs = tic.data['chikou_span']
    cnts = tic.data['tenkan_sen']
    cnks = tic.data['kijun_sen']
    cnssa = tic.data['senkou_span_a']
    cnssb = tic.data['senkou_span_b']
    bw_mfi = tic.data['bw_mfi']
    mfi = tic.data['mfi']
    momentum = tic.data['momentum']
    macd_v = tic.data['macd_value']
    macd_s = tic.data['macd_signal']
    bbu = tic.data['bollinger_up']
    bbm = tic.data['bollinger_mid']
    bbb = tic.data['bollinger_bottom']
    sma = tic.data['sma']
    fr_h = tic.data['fractal_highs']
    fr_l = tic.data['fractal_lows']
    arr = []
    print('len', len(tic.data))
    for i in range(len(tic.data)):
        dic = {}
        dic['open'] = _open[i]
        #dic['date'] = date[i].__str__()
        dic['date'] = date[i].strftime("%Y-%m-%-d")
        #print(dic['open'])
        dic['close'] = close[i]
        dic['high'] = high[i]
        dic['low'] = low[i]
        dic['volume'] = volume[i]
        dic['awesome_oss'] = ao[i]
        dic['accel_oss'] = ac[i]
        dic['accum_dist'] = ad[i]
        dic['avg_true_range'] = atr[i]
        dic['bears_power'] = bep[i]
        dic['bulls_power'] = bup[i]
        dic['commodity_chan_index'] = cci[i]
        dic['demarker'] = dem[i]
        dic['exp_moving_avg'] = ema[i]
        dic['force_index'] = frc[i]
        dic['chikou_span'] = cncs[i]
        dic['tenkan_sen'] = cnts[i]
        dic['kijun_sen'] = cnks[i]
        dic['senkou_span_a'] = cnssa[i]
        dic['senkou_span_b'] = cnssb[i]
        dic['market_facilitation_index'] = bw_mfi[i]
        dic['momentum'] = momentum[i]
        dic['money_flow_index'] = mfi[i]
        dic['macd_value'] = macd_v[i]
        dic['macd_signal'] = macd_s[i]
        dic['bollinger_up'] = bbu[i]
        dic['bollinger_mid'] = bbm[i]
        dic['bollinger_bottom'] = bbb[i]
        dic['sma'] = sma[i]
        dic['fract_high'] = fr_h[i]
        dic['fract_low'] = fr_l[i]



        arr.append(dic)
    for g in arr:
        for key, value in g.items():
            if key == 'date':
                continue
            if value > 0:
                g[key] = int(value*1000) / 1000
            else:
                g[key] = None
    res = {}
    res['data'] = arr
    return res

#run the app
if __name__ == "__main__":
    app.run(debug=True)