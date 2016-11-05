#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import simplejson as json
import redis
from datetime import datetime
import time
from statistics import mean
from ISStreamer.Streamer import Streamer

from twython import Twython, TwythonError

def make_request(URL, CHECK_STRRING):
    USERAGET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
    headers = {'user-agent': USERAGET}

    try:
        response = requests.get(URL, headers=headers, timeout=(2,5))
        if response.status_code == requests.codes.ok:
            if isinstance(response.json(), list):
                if CHECK_STRRING in response.json()[0]:
                    return response.json()[0]

            else:
                if CHECK_STRRING in response.json():
                    return response.json()

    except requests.exceptions.RequestException:
        return None


def get_poloniex():
    URL           = 'https://poloniex.com/public?command=returnTicker'
    CHECK_STRRING = 'BTC_DASH'
    SECON_STRRING = 'USDT_DASH'
    exsymbol      = 'poloniex'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if SECON_STRRING in rawjson:
            valbtc = round(float(rawjson[CHECK_STRRING]['last']), 5)
            valusd = round(float(rawjson[SECON_STRRING]['last']), 2)
            if valbtc > 0 and valusd > 0:
                dashbtc[exsymbol] = valbtc
                dashusd[exsymbol] = valusd


def get_exmo():
    URL           = 'https://api.exmo.com/v1/ticker/'
    CHECK_STRRING = 'DASH_BTC'
    SECON_STRRING = 'DASH_USD'
    exsymbol      = 'exmo'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if SECON_STRRING in rawjson:
            valbtc = round(float(rawjson[CHECK_STRRING]['last_trade']), 5)
            valusd = round(float(rawjson[SECON_STRRING]['last_trade']), 2)
            if valbtc > 0 and valusd > 0:
                dashbtc[exsymbol] = valbtc
                dashusd[exsymbol] = valusd


def get_bittrex():
    URL           = 'https://bittrex.com/api/v1.1/public/getticker?market=btc-dash'
    CHECK_STRRING = 'success'
    exsymbol      = 'bittrex'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if rawjson[CHECK_STRRING] == True:
            valbtc = round(float(rawjson['result']['Last']), 5)
            if valbtc > 0:
                dashbtc[exsymbol] = valbtc


def get_btcebtc():
    URL           = 'https://btc-e.com/api/3/ticker/dsh_btc'
    CHECK_STRRING = 'dsh_btc'
    exsymbol      = 'btce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valbtc = round(float(rawjson[CHECK_STRRING]['last']), 5)
        if valbtc > 0:
            dashbtc[exsymbol] = valbtc


def get_btceusd():
    URL           = 'https://btc-e.com/api/3/ticker/dsh_usd'
    CHECK_STRRING = 'dsh_usd'
    exsymbol      = 'btce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valusd = round(float(rawjson[CHECK_STRRING]['last']), 2)
        if valusd > 0:
            dashusd[exsymbol] = valusd


def get_xbtcebtc():
    URL           = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHBTC'
    CHECK_STRRING = 'Symbol'
    exsymbol      = 'xbtce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if rawjson[CHECK_STRRING] == 'DSHBTC':
            valbtc = round(float(rawjson['BestBid']), 5)
            if valbtc > 0:
               dashbtc[exsymbol] = valbtc 

def get_xbtceusd():
    URL           = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHUSD'
    CHECK_STRRING = 'Symbol'
    exsymbol      = 'xbtce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if rawjson[CHECK_STRRING] == 'DSHUSD':
            valusd = round(float(rawjson['BestBid']), 2)
            if valusd > 0:
               dashusd[exsymbol] = valusd

def get_yobit():
    URL           = 'https://yobit.net/api/2/dash_btc/ticker'
    CHECK_STRRING = 'ticker'
    exsymbol      = 'yobit'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valbtc = round(float(rawjson['ticker']['last']), 5)
        if valbtc > 0:
            dashbtc[exsymbol] = valbtc    


#-----------
def check_redis():
    s = redis.StrictRedis(host=SETINEL_HOST, port=26379, socket_timeout=0.1)
    try:
        h = s.execute_command("SENTINEL get-master-addr-by-name mymaster")[0].decode("utf-8")
        print(h)
        if h == REDIS_MASTER:
            print('Other host is redis master')
            sys.exit()

        else:
            pass

    except Exception as e:
        print(e.args[0])
        sys.exit()

#--------------
def check_update():
    cur_time = time.time()
    lastupdate = json.loads(r.get(r_KEY_DASH_BTC_PRICE))['tstamp']
    if cur_time - lastupdate > 270 and cur_time - lastupdate < 330:
        twitter.update_status(status='ticker btc has prob')

#--------------
key_prefix = 'TICKER:'
r_SS_DASH_BTC_PRICE = key_prefix + 'ss_dash_btc_price'
r_SS_DASH_USD_PRICE = key_prefix + 'ss_dash_usd_price'

r_KEY_DASH_BTC_PRICE = key_prefix + 'key_dash_btc_price'
r_KEY_DASH_USD_PRICE = key_prefix + 'key_dash_usd_price'


# SENTINEL CHECK
# MASTER
SETINEL_HOST = '192.168.10.3'
REDIS_MASTER = '192.168.10.2'

#SLAVE
#SETINEL_HOST = '192.168.10.4'
#REDIS_MASTER = '192.168.10.1'

# ISS
ISS_BUCKET_NAME = 'ticker'
ISS_BUCKET_KEY  = 'xxxxxx'
ISS_BUCKET_AKEY = 'xxxxx'
ISS_PREFIX_BTC  = 'dashbtc'
ISS_PREFIX_USD  = 'dashusd'

streamer = Streamer(bucket_name=ISS_BUCKET_NAME, bucket_key=ISS_BUCKET_KEY, access_key=ISS_BUCKET_AKEY, buffer_size=50)

# twitter
APP_KEY            = 'xxxxx'
APP_SECRET         = 'xxxxx'
OAUTH_TOKEN        = 'xx-xxx'
OAUTH_TOKEN_SECRET = 'xxxxx'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# redis
POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=POOL)

#
dashbtc = {}
dashusd = {}
now = datetime.now()
epoch00 = int(time.mktime(now.timetuple())) - now.second

#
try:
    check_redis()

except Exception as e:
    print(e.args[0])

try:
    check_update()
    get_poloniex()
    get_exmo()
    get_bittrex()
    get_btcebtc()
    get_btceusd()
    get_xbtcebtc()
    get_xbtceusd()
    get_yobit()

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
    try:
        pipe = r.pipeline()
        pipe.set(r_KEY_DASH_BTC_PRICE, json.dumps(dashbtc, sort_keys=True))
        pipe.set(r_KEY_DASH_USD_PRICE, json.dumps(dashusd, sort_keys=True))
        pipe.zadd(r_SS_DASH_BTC_PRICE, epoch00, str(epoch00) + ':' + str(dashbtc['avg']))
        pipe.zadd(r_SS_DASH_USD_PRICE, epoch00, str(epoch00) + ':' + str(dashusd['avg']))
        response = pipe.execute()

    except Exception as e:
        print(e.args[0])
        pass

    # ISS
    try:
        streamer.log_object(dashbtc, key_prefix=ISS_PREFIX_BTC, epoch=epoch00)
        streamer.log_object(dashusd, key_prefix=ISS_PREFIX_USD, epoch=epoch00)
        streamer.flush()
        streamer.close()

    except Exception as e:
        print(e.args[0])
        pass

except Exception as e:
    print(e.args[0])

except KeyboardInterrupt:
    sys.exit()

