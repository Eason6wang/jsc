from __future__ import division

fvList = {"AAPL": [None,None,0,0,0.0002], "BOND": [None,None,0,0,0.0005], "GOOG": [None,None,0,0,0.0002], "MSFT": [None,None,0,0,0.0002], "BABA": [None,None,0,0,0.0005], "BABZ": [None,None,0,0,0.0002], "XLK": [None,None,0,0,0.0006]}


def updateValues(data, symb):
    global fvList
    buys = data['buy']
    sells = data['sell']

    if(len(buys) > 0):
        mean_buy = sum([int(price) for price, size in buys]) / len(buys)
        if(fvList[symb][0] == None):
            fvList[symb][0] = mean_buy
        else:
            fvList[symb][0] = (fvList[symb][0] + mean_buy)/2
    if(len(sells) > 0):
        mean_sell = sum([int(price) for price, size in sells])/ len(sells)
        if(fvList[symb][1] == None):
            fvList[symb][1] = mean_sell
        else:
            fvList[symb][1] = (fvList[symb][1] + mean_sell)/2


def trade_fv(data):
    global fvList
    """Given the data in the book, decides whether we should make a trade.
    Returns a list of trades (buy/sell, symbol, price, size).
    """
    trades = []
    if(data['type'] != 'book' or data['symbol'] == 'BOND'):
        return trades
    symb = data['symbol']
    fv = fvList[symb]

    updateValues(data, symb)
    if(fv[0] == None or fv[1] == None):
        return trades

    fv_s = fvList[symb]
    fv = (fv_s[0]+fv_s[1])/2
    diff = fv * fv_s[4] #0.0001

    for entry in data['buy']:
        if fv_s[3] - fv_s[2] < 12:
            if(int(entry[0]) > fv + diff):
                trades.append(['SELL', symb, entry[0], entry[1]])
                fv_s[3] += int(entry[1])
    for entry in data['sell']:
        if fv_s[2] - fv_s[3] < 12:
            if(int(entry[0]) < fv - diff):
                trades.append(['BUY', symb, entry[0], entry[1]])
                fv_s[2] += int(entry[1])
    #print(fvList)
    return trades

