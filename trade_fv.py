
#mean_buy, mean_sell, bought_size, sold_size, threshold
dic = {"AAPL": [0,0,0,0,0.0002], 
       "BOND": [0,0,0,0,0.0005], 
       "GOOG": [0,0,0,0,0.0002], 
       "MSFT": [0,0,0,0,0.0002], 
       "BABA": [0,0,0,0,0.0005], 
       "BABZ": [0,0,0,0,0.0002], 
       "XLK": [0,0,0,0,0.0005]}
NUMBER_THRES = 10

def change_params(data, s):
    global dic
    buy = data['buy']
    sell = data['sell']
    param = dic[s]
    if len(buy) > 0:
        total_buy = 0
        total_size = 0
        for price, size in buy:
            total_buy += int(price)
            total_size += size
        mean_buy = total_buy / len(buy)
        if param[0] == 0:
            param[0] = mean_buy
        else:
            param[0] = (param[0] + mean_buy) / 2
    if len(sell) > 0:
        total_sell = 0
        total_size = 0
        for price, size in sell:
            total_sell += int(price)
            total_size += size
        mean_sell = total_sell / len(sell)
        if param[1] == 0:
            param[1] = mean_sell
        else:
            param[1] = (param[1] + mean_sell)/2


def trade_fv(data):
    global dic
    trades = []
    if(data['type'] != 'book' or data['symbol'] == 'BOND'):
        return trades
    s = data['symbol']
    change_params(data, s)
    params = dic[s]
    if params[0] == 0 or params[1] == 0:
        return trades
    fv = (params[0]+params[1])/2
    thres = fv * params[4]
    for buy in data['buy']:
        if params[3] - params[2] < NUMBER_THRES:
            if(int(buy[0]) > fv + thres):
                trades.append(['SELL', s, buy[0], buy[1]])
                params[3] += int(buy[1])
    for sell in data['sell']:
        if params[2] - params[3] < NUMBER_THRES:
            if(int(sell[0]) < fv - thres):
                trades.append(['BUY', s, sell[0], sell[1]])
                params[2] += int(sell[1])
    return trades

