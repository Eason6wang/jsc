

def trade_adr(data):
    if data['type'] == 'book'and data['symbol'] == 'BOND':
        sell = data['sell']
        buy = data['buy']
        trades = []
        for batch in sell:
            output = {}
            if int(batch[0]) < 1000:
                output = ['BUY', 'BOND', int(batch[0]), int(batch[1])]
                trades.append(output)
                print("BUYING BOND")
        for batch in buy:
            output = {}
            if int(batch[0]) > 1000:
            output = ['SELL', 'BOND', int(batch[0]), int(batch[1])]
            trades.append(output)
            print("SELLING BOND")
        return trades
    return []

