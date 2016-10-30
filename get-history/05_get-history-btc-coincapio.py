#!/usr/bin/env python3
import sys
import time
import datetime
import json
import socket
import re
import urllib.request as urlopen
#---
def getdata():
    url = "http://www.coincap.io/history/BTC"
    request  = urlopen.Request(url)
    request.add_header('User-agent', 'Mozilla/6.0 Safari/5.17')

    try:
        response = urlopen.urlopen(request, None, 60)
        r = json.loads(response.read().decode('utf-8'))
        if r:
            #print(json.dumps(r['price'], sort_keys=True, indent=4, separators=(',', ': ')))    
            filetow = 'btc_coincapio_history.log'
            with open(filetow, 'w') as fp:
                json.dump(r, fp)

    except Exception as e:
        print(e.args[0])
        sys.exit(1)

try:
    getdata()

except Exception as e:
    print(e.args[0])
    sys.exit(1)

