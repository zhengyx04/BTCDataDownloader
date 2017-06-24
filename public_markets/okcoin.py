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
        xt=datetime.datetime.utcnow()
        url = 'https://www.okcoin.cn/api/v1/depth.do?symbol='+ticker+'&size=20'
        res = urllib.request.urlopen(url).read().decode('utf8')
        depth = json.loads(res)
        return self.transform_depth(xt,depth)

    def transform_depth(self,xt,depth):
        res = {'xt':xt, 'asks':[], 'bids':[]}
        if len(depth['asks']) > 0:
            res['asks'] = [{'price':float(e[0]), 'size':float(e[1]), 'timestamp':None} for e in depth['asks']]
        if len(depth['bids']) > 0:
            res['bids'] = [{'price':float(e[0]), 'size':float(e[1]), 'timestamp':None} for e in depth['bids']]
        return res if len(res['bids'])>0 or len(res['asks'])>0 else None

    #def get_currency_pair(self,ticker):
    #    return 'pccy','occy'

    @staticmethod
    def create():
        return OKCoin()

Market.register_market(OKCoin)

if __name__   == "__main__":
    pass

