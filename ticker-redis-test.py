#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import time
import sys
import simplejson as json
import redis

import pprint


key_prefix = 'TICKER:'
r_SS_BTC_PRICE = key_prefix + 'ss_btc_price'
r_KEY_BTC_PRICE = key_prefix + 'key_btc_price'


r_SS_DASH_BTC_PRICE = key_prefix + 'ss_dash_btc_price'
r_SS_DASH_USD_PRICE = key_prefix + 'ss_dash_usd_price'

r_KEY_DASH_BTC_PRICE = key_prefix + 'key_dash_btc_price'
r_KEY_DASH_USD_PRICE = key_prefix + 'key_dash_usd_price'

# redis
POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=POOL)

pp = pprint.PrettyPrinter(indent=4)

#r.flushdb()
#sys.exit()

def check_redis():
    s = redis.StrictRedis(host='192.168.10.4', port=26379, socket_timeout=0.1)
    h = s.execute_command("SENTINEL get-master-addr-by-name mymaster")[0].decode("utf-8")
#    if h == '192.168.10.1':
#        sys.exit()    

check_redis()

try:

#
    print('r_SS_DASH_BTC_PRICE')
    pp.pprint(r.zrange(r_SS_DASH_BTC_PRICE, 0, -1, withscores=True))

    print('r_KEY_DASH_BTC_PRICE')
    pp.pprint(r.get(r_KEY_DASH_BTC_PRICE))

    print('r_SS_DASH_USD_PRICE')
    pp.pprint(r.zrange(r_SS_DASH_USD_PRICE, 0, -1, withscores=True))

    print('r_KEY_DASH_USD_PRICE')
    pp.pprint(r.get(r_KEY_DASH_USD_PRICE))
#
    print('r_SS_BTC_PRICE')
    pp.pprint(r.zrange(r_SS_BTC_PRICE, 0, -1, withscores=True))

    print('r_KEY_BTC_PRICE')
    x = json.loads(r.get(r_KEY_BTC_PRICE))

    print(x)
    
    pp.pprint(r.get(r_KEY_BTC_PRICE))

except Exception as e:
    print(e.args[0])
    sys.exit()

except KeyboardInterrupt:
    sys.exit(1)

