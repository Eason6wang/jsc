BOUGHT_BOND = 0
SOLD_BOND = 0

def trade_bond(data):
    global BOUGHT_BOND, SOLD_BOND
    if data['type'] == 'book'and data['symbol'] == 'BOND':
        sell = data['sell']
        buy = data['buy']
        trades = []
        for batch in sell:
            output = {}
            if BOUGHT_BOND - SOLD_BOND < 5:
                if int(batch[0]) < 1000:
                    output = ['BUY', 'BOND', int(batch[0]), int(batch[1])]
                    trades.append(output)
                    print("BUYING BOND")
                    BOUGHT_BOND += int(batch[1])
        for batch in buy:
            output = {}
            if SOLD_BOND - BOUGHT_BOND < 5:
                if int(batch[0]) > 1000:
                    output = ['SELL', 'BOND', int(batch[0]), int(batch[1])]
                    trades.append(output)
                    print("SELLING BOND")
                    SOLD_BOND += int(batch[1])
        return trades
    return []
