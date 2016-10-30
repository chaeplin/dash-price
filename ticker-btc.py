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
from ISStreamer.Streamer import Streamer

#   https://api.bitfinex.com/v1/pubticker/BTCUSD
#   https://api.gdax.com/products/BTC-USD/ticker
#   https://btc-e.com/api/3/ticker/btc_usd
#   https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/BTCUSD
#   https://www.bitstamp.net/api/v2/ticker_hour/btcusd/
#   https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd


USERAGET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'

def get_bitfinex():
    start_time = time()
    url = 'https://api.bitfinex.com/v1/pubticker/BTCUSD'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
#        print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'last_price' in r:
            valusd = round(float(r['last_price']), 2)
            if valusd > 0:
                rawjson['vusd'] = valusd

        return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return rawjson


def get_gdax():
    start_time = time()
    url = 'https://api.gdax.com/products/BTC-USD/ticker'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
#        print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'price' in r:
            valusd = round(float(r['price']), 2)
            if valusd > 0:
                rawjson['vusd'] = valusd

        return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return rawjson


def get_btce():
    start_time = time()
    url = 'https://btc-e.com/api/3/ticker/btc_usd'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
#        print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'last' in r['btc_usd']:
            valusd = round(float(r['btc_usd']['last']), 2)
            if valusd > 0:
                rawjson['vusd'] = valusd

        return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return rawjson


def get_xbtce():
    start_time = time()
    url = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/BTCUSD'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)
    request.add_header('Accept-Encoding', 'gzip')

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(gzip.decompress(response.read()).decode('utf-8'))[0]
#        print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'Symbol' in r:
            if r['Symbol'] == 'BTCUSD':
                valbtc = round(float(r['BestBid']), 2)
                if valbtc > 0:
                    rawjson['vusd'] = valbtc

        return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return rawjson


def get_bitstamp():
    start_time = time()
    url = 'https://www.bitstamp.net/api/v2/ticker_hour/btcusd/'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
#        print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'last' in r:
            valusd = round(float(r['last']), 2)
            if valusd > 0:
                rawjson['vusd'] = valusd

        return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return rawjson

def get_okcoin():
    start_time = time()
    url = 'https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd'
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    rawjson = {}
    rawjson['vusd']  = -1

    try:
        response = urlopen.urlopen(request, timeout=2)
        r = json.loads(response.read().decode('utf-8'))
#        print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)

        if r and 'ticker' in r:
            valusd = round(float(r['ticker']['last']), 2)
            if valusd > 0:
                rawjson['vusd'] = valusd

        return rawjson

    except Exception as e:
        stop_time = time()
        rawjson['t']  = round((stop_time - start_time), 3)
        print(e.args[0])
        return rawjson


# main
btcusd = {}

try:
    bitfinex = get_bitfinex()
    if  bitfinex['vusd'] > 0:
        btcusd['bitfinex'] = bitfinex['vusd']

    gdax = get_gdax()
    if gdax['vusd'] > 0:
        btcusd['gdax'] = gdax['vusd']

    btce = get_btce()
    if btce['vusd'] > 0:
        btcusd['btce'] = btce['vusd']

    xbtce = get_xbtce()
    if xbtce['vusd'] > 0:
        btcusd['xbtce'] = xbtce['vusd']

    bitstamp = get_bitstamp()
    if bitstamp['vusd'] > 0:
        btcusd['bitstamp'] = bitstamp['vusd']

    okcoin = get_okcoin()
    if okcoin['vusd'] > 0:
        btcusd['okcoin'] = okcoin['vusd']

    l_btcusd = []
    for key in btcusd:
        l_btcusd.append(btcusd[key])

    btcusd['avg'] = round(mean(sorted(l_btcusd)[1:-1]), 2)

    streamer = Streamer(bucket_name='ticker', bucket_key='xxxx', access_key='xxxx', buffer_size=50)
    streamer.log_object_no_ub(btcusd, key_prefix="btcusd_")
    streamer.close()

except Exception as e:
    print(e.args[0])

