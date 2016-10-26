#!/usr/bin/env python3
import sys
import datetime
import json
import socket
import re
from time import time, sleep
from bs4 import BeautifulSoup
import socket
import urllib.request as urlopen

USERAGET = "Mozilla/6.0 Safari/5.17"

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

def getpoloniex():
    url = "https://poloniex.com/public?command=returnTicker"
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    poloniex = {}

    try:
        response = urlopen.urlopen(request, None, 2)
        r = json.loads(response.read().decode('utf-8'))
        if r:
            dash = round(float(r['BTC_DASH']['last']), 5)
            if r:
                poloniex['poloniexdashbtc'] = dash
                return poloniex
            else:
                return None
        else:
            return None

    except Exception as e:
        print(e.args[0])
        return None


def getcryptowatch():
    url = "https://cryptowat.ch/poloniex/dashbtc"
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    cryptowatch = {}
    BitMEX = Bitfinex = BTCe = Coinbase = DASH = '0'

    try:
        response = urlopen.urlopen(request, None, 2)
        r = response.read().decode('utf-8')
        if r:
            soup = BeautifulSoup(r, 'html.parser')
            header = soup.header

            letters = soup.find_all("div", class_="nav-category")

            for x in letters:
                y = x.get_text().replace("\n\n", "").replace("\n", "").replace("\t", "").replace(" ", "")
                if y.startswith('BTCFuturesOKCoinUS'):
                    BitMEX = re.search(r'XBTUSD(.*)XBJ24H', y)
                    if BitMEX != '0':
                        cryptowatch['BitMEXbtcusd'] = float(BitMEX.group(1))

                if y.startswith('BTCBitfinexUSD'):
                    Bitfinex = re.search(r'BTCBitfinexUSD(.*)CoinbaseUSD', y)
                    BTCe     = re.search(r'BTC-eUSD(.*)CEX', y)
                    Coinbase = re.search(r'CoinbaseUSD(.*)EUR(.*)CAD(.*)GBP(.*)BitstampUSD', y)

                    if Bitfinex != '0':
                        cryptowatch['Bitfinexbtcusd'] = float(Bitfinex.group(1))

                    if BTCe != '0':
                        cryptowatch['BTCebtcusd'] = float(BTCe.group(1))

                    if Coinbase != '0':
                        cryptowatch['Coinbasebtcusd'] = float(Coinbase.group(1))

                if y.startswith('DASHPoloniexBTC'):
                    DASH     = re.search(r'DASHPoloniexBTC(.*)$', y)
                    if DASH != '0':
                        cryptowatch['DASHcwbtc'] = float(DASH.group(1))


            return cryptowatch

        else:
            return None

    except Exception as e:
        print(e.args[0])
        return None

def getcoincapio():
    url = "http://www.coincap.io/page/DASH"
    request  = urlopen.Request(url)
    request.add_header('User-agent', USERAGET)

    coincapio = {}

    try:
        response = urlopen.urlopen(request, None, 2)
        r = json.loads(response.read().decode('utf-8'))
        if r:
            btcPrice = float(r['btcPrice'])
            usdPrice = float(r['usdPrice'])

            if btcPrice > 0 and usdPrice > 0:
                dashbtc = round((usdPrice / btcPrice), 5)
                coincapio['coincapbtcusd']  = btcPrice
                coincapio['coincapdashusd'] = round(usdPrice,3) 
                coincapio['coincapdashbtc'] = dashbtc
                
                return coincapio

            else:
                return None

        else:
            return None

    except Exception as e:
        print(e.args[0])
        return None


try:
    start_poloniex = time()
    poloniex=getpoloniex()
    time_poloniex = time() - start_poloniex

   
    start_cryptowatch = time() 
    cryptowatch=getcryptowatch()
    time_cryptowatch = time() - start_cryptowatch
   
    start_coincapio = time() 
    coincapio=getcoincapio()
    time_coincapio = time() - start_coincapio

    payload = "price,mainnet=true "

    if poloniex:
        poloniex_key = poloniex.keys()
        for poloniex_key in poloniex:
            payload += poloniex_key + "=" + str(poloniex[poloniex_key]) + ","

    if cryptowatch:
        cryptowatch_key = cryptowatch.keys()
        for cryptowatch_key in cryptowatch:
            payload += cryptowatch_key + "=" + str(cryptowatch[cryptowatch_key]) + ","

    if coincapio:
        coincapio_key = coincapio.keys()
        for coincapio_key in coincapio:
            payload += coincapio_key + "=" + str(coincapio[coincapio_key]) + ","

    payload += "time_poloniex=" + str(time_poloniex) + ","
    payload += "time_cryptowatch=" + str(time_cryptowatch) + ","
    payload += "time_coincapio=" + str(time_coincapio)
    
    print(start_poloniex, payload)
    sendUdpmsg(payload)

except Exception as e:
    print(e.args[0])

