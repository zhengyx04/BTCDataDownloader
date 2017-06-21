import json
import time
import base64
import hashlib
import urllib
import datetime
from .market import Market


class OKCoin(Market):
    def __init__(self):
        super().__init__()
        #self.get_api_root_URL=''

    def get_exchange_depth(self,ticker):
        """
        :param ticker get order book from exchange and format the result
        :return: {'xt','asks':[{'price0','size0'},{'price1','size1'}],'bids':[{'price0','size0'},{'price1','size1'}]}
        """
        url = 'https://www.okcoin.cn/api/v1/depth.do?symbol='+ticker+'&size=20'
        res = urllib.request.urlopen(url).read().decode('utf8')
        res = json.loads(res)
        depth = self.transform_depth(res)
        return depth

    def transform_depth(self,depth):
        res = {'xt':None}
        res['asks'] = [{'price':float(e[0]), 'size':float(e[1]), 'timestamp':None} for e in depth['asks']]
        res['bids'] = [{'price':float(e[0]), 'size':float(e[1]), 'timestamp':None} for e in depth['bids']]
        return res

    #def get_currency_pair(self,ticker):
    #    return 'pccy','occy'

    @staticmethod
    def create():
        return OKCoin()

Market.register_market(OKCoin)

if __name__   == "__main__":
    pass

