import json
import time
import base64
import hashlib
import urllib
import datetime
from .market import Market


class Huobi(Market):
    def __init__(self):
        super().__init__()
        #self.get_api_root_URL=''

    def get_exchange_depth(self,ticker):
        """
        :param ticker get order book from exchange and format the result
        :return: {'xt','asks':[{'price0','size0'},{'price1','size1'}],'bids':[{'price0','size0'},{'price1','size1'}]}
        """
        if ticker == 'btccny':
            url = 'http://api.huobi.com/staticmarket/depth_btc_20.js'
        elif ticker == 'ltccny':
            url = 'http://api.huobi.com/staticmarket/depth_ltc_20.js'
        elif ticker == 'btcusd':
            url = 'http://api.huobi.com/usdmarket/depth_btc_20.js'
        else:
            url = ''
        res = urllib.request.urlopen(url).read().decode('utf8')            
        depth = json.loads(res)
        return self.transform_depth(depth)

    def transform_depth(self,depth):
        #print(float(depth['ts']))
        res = {'xt':datetime.datetime.utcfromtimestamp(float(depth['ts'])/1000), 'asks':[], 'bids':[]}
        if len(depth['asks']) > 0:
            res['asks'] = [{'price':float(e[0]), 'size':float(e[1]), 'timestamp':None} for e in depth['asks']]
        if len(depth['bids']) > 0:
            res['bids'] = [{'price':float(e[0]), 'size':float(e[1]), 'timestamp':None} for e in depth['bids']]
        return res if len(res['bids'])>0 or len(res['asks'])>0 else None

    #def get_currency_pair(self,ticker):
    #    return 'pccy','occy'

    @staticmethod
    def create():
        return Huobi()

Market.register_market(Huobi)

if __name__   == "__main__":
    pass

