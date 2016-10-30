#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import simplejson as json
import redis
import socket
import re
from datetime import datetime
import time
from bs4 import BeautifulSoup
import socket
import urllib.request as urlopen
import gzip
from statistics import mean
from ISStreamer.Streamer import Streamer

#   https://poloniex.com/public?command=returnTicker
#   https://api.exmo.com/v1/ticker/
#   https://bittrex.com/api/v1.1/public/getticker?market=btc-dash
#   https://btc-e.com/api/3/ticker/dsh_btc
#   https://btc-e.com/api/3/ticker/dsh_usd
#   https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHBTC
#   https://yobit.net/api/2/dash_btc/ticker

USERAGET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'

key_prefix = 'TICKER:'
r_SS_DASH_BTC_PRICE = key_prefix + 'ss_dash_btc_price'
r_SS_DASH_USD_PRICE = key_prefix + 'ss_dash_usd_price'
r_HA_DASH_BTC_PRICE = key_prefix + 'ha_dash_btc_price'
r_HA_DASH_USD_PRICE = key_prefix + 'ha_dash_usd_price'

# redis
POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=POOL)

def get_poloniex():
    start_time = time.time()
    url = 'https://poloniex.com/public?command=returnTicker'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'BTC_DASH' in r and 'USDT_DASH' in r:
            valbtc = round(float(r['BTC_DASH']['last']), 5)
            valusd = round(float(r['USDT_DASH']['last']), 2)
            if valbtc > 0 and valusd > 0:
                rawjson['vbtc'] = valbtc
                rawjson['vusd'] = valusd

                return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_exmo():
    start_time = time.time()
    url = 'https://api.exmo.com/v1/ticker/'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'last_trade' in r['DASH_BTC'] and 'last_trade' in r['DASH_USD']:
            valbtc = round(float(r['DASH_BTC']['last_trade']), 5)
            valusd = round(float(r['DASH_USD']['last_trade']), 2)
            if valbtc > 0 and valusd > 0:
                rawjson['vbtc'] = valbtc
                rawjson['vusd'] = valusd

                return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_bittrex():
    start_time = time.time()
    url = 'https://bittrex.com/api/v1.1/public/getticker?market=btc-dash'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'success' in r:
            if r['success'] == True:
                valbtc = round(float(r['result']['Last']), 5)
                if valbtc > 0:
                    rawjson['vbtc'] = valbtc

                    return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None


def get_btcebtc():
    start_time = time.time()
    url = 'https://btc-e.com/api/3/ticker/dsh_btc'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        
        if r and 'dsh_btc' in r:
            valbtc = round(float(r['dsh_btc']['last']), 5)
            if valbtc > 0:
                rawjson['vbtc'] = valbtc

                return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None


def get_btceusd():
    start_time = time.time()
    url = 'https://btc-e.com/api/3/ticker/dsh_usd'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        
        if r and 'dsh_usd' in r:
            valbtc = round(float(r['dsh_usd']['last']), 2)
            if valbtc > 0:
                rawjson['vusd'] = valbtc

                return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_xbtcebtc():
    start_time = time.time()
    url = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHBTC'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)
    request.add_header('Accept-Encoding', 'gzip')

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(gzip.decompress(response.read()).decode('utf-8'))[0]
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'Symbol' in r:
            if r['Symbol'] == 'DSHBTC':
                valbtc = round(float(r['BestBid']), 5)
                if valbtc > 0:
                    rawjson['vbtc'] = valbtc

                    return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_xbtceusd():
    start_time = time.time()
    url = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHUSD'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)
    request.add_header('Accept-Encoding', 'gzip')

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(gzip.decompress(response.read()).decode('utf-8'))[0]
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'Symbol' in r:
            if r['Symbol'] == 'DSHUSD':
                valbtc = round(float(r['BestBid']), 2)
                if valbtc > 0:
                    rawjson['vusd'] = valbtc

                    return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None

def get_yobit():
    start_time = time.time()
    url = 'https://yobit.net/api/2/dash_btc/ticker'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vbtc']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'ticker' in r:
            valbtc = round(float(r['ticker']['last']), 5)
            if valbtc > 0:
                rawjson['vbtc'] = valbtc

                return rawjson

    except Exception as e:
        stop_time = time.time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return None


# main
dashbtc = {}
dashusd = {}
now = datetime.now()
epoch00 = int(time.mktime(now.timetuple())) - now.second

try:

    poloniex = get_poloniex()
    if poloniex and poloniex['vbtc'] > 0 and poloniex['vusd'] > 0:
        dashbtc['poloniex'] = poloniex['vbtc']
        dashusd['poloniex'] = poloniex['vusd']

    exmo = get_exmo()
    if exmo and exmo['vbtc'] > 0 and exmo['vusd'] > 0:
        dashbtc['exmo'] = exmo['vbtc']
        dashusd['exmo'] = exmo['vusd']

    bittrex = get_bittrex()
    if bittrex and bittrex['vbtc'] > 0:
        dashbtc['bittrex'] = bittrex['vbtc']

    btcebtc = get_btcebtc() 
    if btcebtc and btcebtc['vbtc'] > 0:
        dashbtc['btce'] = btcebtc['vbtc']

    btceusd = get_btceusd()
    if btceusd and btceusd['vusd'] > 0:
        dashusd['btce'] = btceusd['vusd']

    xbtcebtc = get_xbtcebtc()
    if xbtcebtc and xbtcebtc['vbtc'] > 0:
        dashbtc['xbtce'] = xbtcebtc['vbtc']

    xbtceusd = get_xbtceusd()
    if xbtceusd and xbtceusd['vusd'] > 0:
        dashusd['xbtce'] = xbtceusd['vusd']

    yobit = get_yobit()
    if yobit and yobit['vbtc'] > 0:
        dashbtc['yobit'] = yobit['vbtc']

    l_dashbtc = []
    for key in dashbtc:
        l_dashbtc.append(dashbtc[key])

    l_dashusd = []
    for key in dashusd:
        l_dashusd.append(dashusd[key])

    dashbtc['avg'] = round(mean(sorted(l_dashbtc)[1:-1]), 5)
    dashusd['avg'] = round(mean(sorted(l_dashusd)[1:-1]), 2)

    dashbtc['tstamp'] = dashusd['tstamp'] = epoch00

    # redis
    pipe = r.pipeline()
    pipe.hset(r_HA_DASH_BTC_PRICE, epoch00, dashbtc)
    pipe.hset(r_HA_DASH_USD_PRICE, epoch00, dashusd)
    pipe.zadd(r_SS_DASH_BTC_PRICE, epoch00, str(epoch00) + ':' + str(dashbtc['avg']))
    pipe.zadd(r_SS_DASH_USD_PRICE, epoch00, str(epoch00) + ':' + str(dashusd['avg']))
    response = pipe.execute()

    # ISS
    streamer = Streamer(bucket_name='ticker', bucket_key='5YS94TRX3T7V', access_key='4V4zdLdXD1wA7P2gZ8AatkIiouP6WK77', buffer_size=50)
    streamer.log_object_no_ub(dashbtc, key_prefix="dashbtc_", epoch=epoch00)
    streamer.log_object_no_ub(dashusd, key_prefix="dashusd_", epoch=epoch00)
    streamer.close()

except Exception as e:
    print(e.args[0])
    sys.exit()

except KeyboardInterrupt:
    sys.exit()

