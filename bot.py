#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="THREEZEROZEROTWO"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = False
print(test_mode)

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# ~~~~~============== MAIN LOOP ==============~~~~~

import pdb
oid = 1

def trade(exchange, action, symbol, price, size):
    global oid
    trade = {'type': 'add', 'order_id': oid, 'symbol': symbol,
					 'dir': action, 'price': price, 'size': size}
    oid += 1
    #print(trade)
    write_to_exchange(exchange, trade)


def trade_batch(exchange, trades):
    for buysell, symbol, price, size in trades:
        if buysell and size != 0:
            trade(exchange, buysell, symbol, price, size)

from strategy import trade_bond
from trade_fv import trade_fv

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    print(hello_from_exchange)
    strategies = [trade_fv]
    strategies += [trade_bond]

    data = read_from_exchange(exchange)
    while data:
        #check type
        #print(data)
        if data['type'] == 'error' or data['type'] == 'fill' or data['type'] == 'reject' or data['type'] == 'ack':
            print(data)
        if data['type'] != 'book': 
            data = read_from_exchange(exchange)
            continue
        trades = []
        for strategy in strategies:
            #pdb.set_trace()
            trades.extend(strategy(data))
            trade_batch(exchange, trades)
            data = read_from_exchange(exchange)

if __name__ == "__main__":
    main()

