#!/usr/bin/env python3
import sys
import datetime
import json
import socket
import re
from time import time, sleep
from pprint import pprint

def sendUdpmsg(msgtosend):
    IPADDR = '127.0.0.1'
    PORTNUM = 8089
    PACKETDATA = msgtosend
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.sendto(bytes(PACKETDATA, "utf-8"), (IPADDR, PORTNUM))
    except:
        print ("errors") 

    s.close()


def getload():
    with open('btc_poloniex_history.log') as data_file:    
        data = json.load(data_file)
    
    for x in data:
        payload = "pricehistory,mainnet=true btc_poloniex=" + str(x['weightedAverage']) + " " + str(x['date']*1000000000)
        sendUdpmsg(payload)
        sleep(0.0001)

try:
    getload()

except Exception as e:
    print(e.args[0])
    sys.exit(1)


