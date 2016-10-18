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
    #startepoch = str(int(time.mktime(time.strptime('2014-02-01 00:00:00', '%Y-%m-%d %H:%M:%S'))))
    startepoch = '1391806500'
    url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_DASH&start=" + startepoch + "&end=9999999999&period=300"
    request  = urlopen.Request(url)
    request.add_header('User-agent', 'Mozilla/6.0 Safari/5.17')

    try:
        response = urlopen.urlopen(request, None, 30)
        r = json.loads(response.read().decode('utf-8'))
        if r:
            #print(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))    
            filetow = 'poloniexhistory.log'
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
