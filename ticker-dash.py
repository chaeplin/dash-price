#!/usr/bin/env python3
import socket
import sys
import datetime
import json
import socket
import re
from time import time, sleep
from bs4 import BeautifulSoup
import socket
import urllib.request as urlopen
import gzip
from statistics import mean

#   https://poloniex.com/public?command=returnTicker
#   https://api.exmo.com/v1/ticker/
#   https://bittrex.com/api/v1.1/public/getticker?market=btc-dash
#   https://btc-e.com/api/3/ticker/dsh_btc
#   https://btc-e.com/api/3/ticker/dsh_usd
#   https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHBTC
#   https://yobit.net/api/2/dash_btc/ticker

USERAGET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'

def get_poloniex():
    start_time = time()
    url = 'https://poloniex.com/public?command=returnTicker'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'BTC_DASH' in r and 'USDT_DASH' in r:
            valbtc = round(float(r['BTC_DASH']['last']), 5)
            valusd = round(float(r['USDT_DASH']['last']), 2)
            if valbtc > 0 and valusd > 0:
                rawjson['vbtc'] = valbtc
                rawjson['vusd'] = valusd

                return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_exmo():
    start_time = time()
    url = 'https://api.exmo.com/v1/ticker/'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'last_trade' in r['DASH_BTC'] and 'last_trade' in r['DASH_USD']:
            valbtc = round(float(r['DASH_BTC']['last_trade']), 5)
            valusd = round(float(r['DASH_USD']['last_trade']), 2)
            if valbtc > 0 and valusd > 0:
                rawjson['vbtc'] = valbtc
                rawjson['vusd'] = valusd

                return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_bittrex():
    start_time = time()
    url = 'https://bittrex.com/api/v1.1/public/getticker?market=btc-dash'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'success' in r:
            if r['success'] == True:
                valbtc = round(float(r['result']['Last']), 5)
                if valbtc > 0:
                    rawjson['vbtc'] = valbtc

                    return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None


def get_btcebtc():
    start_time = time()
    url = 'https://btc-e.com/api/3/ticker/dsh_btc'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        
        if r and 'dsh_btc' in r:
            valbtc = round(float(r['dsh_btc']['last']), 5)
            if valbtc > 0:
                rawjson['vbtc'] = valbtc

                return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None


def get_btceusd():
    start_time = time()
    url = 'https://btc-e.com/api/3/ticker/dsh_usd'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        
        if r and 'dsh_usd' in r:
            valbtc = round(float(r['dsh_usd']['last']), 2)
            if valbtc > 0:
                rawjson['vusd'] = valbtc

                return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_xbtcebtc():
    start_time = time()
    url = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHBTC'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)
    request.add_header('Accept-Encoding', 'gzip')

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(gzip.decompress(response.read()).decode('utf-8'))[0]
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'Symbol' in r:
            if r['Symbol'] == 'DSHBTC':
                valbtc = round(float(r['BestBid']), 5)
                if valbtc > 0:
                    rawjson['vbtc'] = valbtc

                    return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_xbtceusd():
    start_time = time()
    url = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHUSD'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)
    request.add_header('Accept-Encoding', 'gzip')

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(gzip.decompress(response.read()).decode('utf-8'))[0]
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'Symbol' in r:
            if r['Symbol'] == 'DSHUSD':
                valbtc = round(float(r['BestBid']), 5)
                if valbtc > 0:
                    rawjson['vusd'] = valbtc

                    return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_yobit():
    start_time = time()
    url = 'https://yobit.net/api/2/dash_btc/ticker'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'ticker' in r:
            valbtc = round(float(r['ticker']['last']), 5)
            if valbtc > 0:
                rawjson['vbtc'] = valbtc

                return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None


# main
dashbtc = {}
dashusd = {}

try:

    poloniex = get_poloniex()

    if len(poloniex) > 1:
        dashbtc['poloniex'] = poloniex['vbtc']
        dashusd['poloniex'] = poloniex['vusd']

    exmo = get_exmo()
    if len(exmo) > 1:
        dashbtc['exmo'] = exmo['vbtc']
        dashusd['exmo'] = exmo['vusd']

    bittrex = get_bittrex()
    if len(bittrex) > 1:
        dashbtc['bittrex'] = bittrex['vbtc']


    btcebtc = get_btcebtc() 
    if len(btcebtc) > 1:
        dashbtc['btce'] = btcebtc['vbtc']

    btceusd = get_btceusd()
    if len(btceusd) > 1:
        dashusd['btce'] = btceusd['vusd']

    xbtcebtc = get_xbtcebtc()
    if len(xbtcebtc) > 1:
        dashbtc['xbtce'] = xbtcebtc['vbtc']

    xbtceusd = get_xbtceusd()
    if len(xbtceusd) > 1:
        dashusd['xbtce'] = xbtceusd['vusd']

    yobit = get_yobit()
    if len(yobit) > 1:
        dashbtc['yobit'] = yobit['vbtc']

    l_dashbtc = []
    for key in dashbtc:
        l_dashbtc.append(dashbtc[key])

    print(round(mean(sorted(l_dashbtc)[1:-1]), 5))

    l_dashusd = []
    for key in dashusd:
        l_dashusd.append(dashusd[key])

    print(round(mean(sorted(l_dashusd)[1:-1]), 2))

except Exception as e:
    print(e.args[0])
    sys.exit()

except KeyboardInterrupt:
    sys.exit()
