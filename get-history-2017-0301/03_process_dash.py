#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import simplejson as json
from datetime import datetime
import time

def timecheck(epoch_):
    date_last_entry = datetime.utcfromtimestamp(epoch_)

    t_day    = str(date_last_entry.day)
    t_month  = str(date_last_entry.month)
    t_year   = str(date_last_entry.year)

    fndate = t_year + '-' + t_month + '-' + t_day

    return fndate

def getload_btcusd():
    with open(filebtcusd) as data_file:
        data = json.load(data_file)

    btcusd ={}

    for x in data['price_usd']:
        date = int(x[0] / 1000)
        Avg  = x[1]

        btcusd[timecheck(date)] = Avg

    return btcusd

def getload_dashbtc():
    with open(filedashbtc) as data_file:
        data = json.load(data_file)

    dashbtc = {}
    prev_val = 0

    for x in data:
        date = x['date']
        Avg  = x['weightedAverage']

        if Avg > 0:
            prev_val = Avg

        if Avg == 0:
            Avg = prev_val

        dashbtc[date] = Avg

    return dashbtc

#-------------------------------------------------------------------
# FILE TO SAVE
filedashbtc = 'dash_btc_poloniex_history.log'
filebtcusd  = 'btc_coinmarketcap_history.log'

file_dash_btc_usd = 'dash_btc_usd_history.log'

try:
    btc_usd_all  = getload_btcusd()
    dash_btc_all = getload_dashbtc()

    prev = 0

    dash_btc_usd = {}

    for x in dash_btc_all:
        epoch_dash  = x
        date_dash   = timecheck(x)
        date_btcusd = btc_usd_all.get(date_dash, None)

        if date_btcusd != None:
            prev = date_btcusd

        if date_btcusd == None:
            date_btcusd = prev

        dash_btc_day = dash_btc_all[x]
        dash_usd_day = round(date_btcusd * dash_btc_day, 2)

        dash_btc_usd[epoch_dash] = {
                "btc": dash_btc_day,
                "usd": dash_usd_day
                }

    with open(file_dash_btc_usd, 'w') as fp:
        json.dump(dash_btc_usd, fp)


except Exception as e:
    print(e.args[0])
    sys.exit()

except KeyboardInterrupt:
    sys.exit()

