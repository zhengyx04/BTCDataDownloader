import urllib.request
import json

def get_prodList(exchange):

    prodList = {}
    prodList['GDAX'] = ['BTC-GBP','BTC-USD','ETH-USD','LTC-USD','ETH-EUR','LTC-EUR','BTC-EUR','ETH-BTC','LTC-BTC']

    res = urllib.request.urlopen('https://api.kraken.com/0/public/AssetPairs')
    jsonstr = res.read().decode('utf8')
    asset = json.loads(jsonstr)
    prodList['Kraken'] = list(asset['result'].keys())
  
    res = urllib.request.urlopen('https://api.bitfinex.com/v1/symbols_details')
    jsonstr = res.read().decode('utf8')
    asset = json.loads(jsonstr)
    prodList['Bitfinex'] = [e['pair'] for e in asset]
  
    return prodList[exchange]

### Examples:
#get_prodList('GDAX')
#get_prodList('Kraken')
#get_prodList('Bitfinex')
