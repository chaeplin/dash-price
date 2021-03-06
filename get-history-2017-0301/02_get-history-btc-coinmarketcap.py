#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import simplejson as json
from datetime import datetime
import time

def make_request():
    URL        = "https://api.coinmarketcap.com/v1/datapoints/bitcoin/"
    USERAGET   = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
    headers    = {'user-agent': USERAGET}

    try:
        response = requests.get(URL, headers=headers)
        if response.status_code == requests.codes.ok:
            with open(filetow, 'w') as fp:
                json.dump(response.json(), fp)

    except requests.exceptions.RequestException:
        print(e.args[0])
        sys.exit(1)

    except Exception as e:
        print(e.args[0])
        sys.exit(1)

#-------------------------------------------------------------------
# FILE TO SAVE
filetow = 'btc_coinmarketcap_history.log'


#
try:
    make_request()
    pass

except Exception as e:
    print(e.args[0])
    sys.exit()

except KeyboardInterrupt:
    sys.exit()

