import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class Bitfinex(Market):
    def __init__(self):
        super().__init__()
        self.get_api_url_orderbook='https://api.bitfinex.com/v1/book/{ticker:s}/?limit_bids=20&limit_asks=20'

    def get_exchange_depth(self,ticker):
        xt=datetime.datetime.utcnow()
        url=self.get_api_url_orderbook.format(ticker=ticker)
        res = urllib.request.urlopen(url).read().decode('utf8')
        depth=json.loads(res)
        return self.depth_transform(xt,depth)

    def depth_transform(self,xt,depth):
        res = {'xt': xt, 'asks':[], 'bids':[]}
        if len(depth['asks']) > 0:
            res['xt'] = datetime.datetime.utcfromtimestamp(float(depth['asks'][0]['timestamp']))
            res['asks']=[ {'price':float(e['price']),'size':float(e['amount']),\
             'timestamp':float(e['timestamp'])} for e in depth['asks']]
        if len(depth['bids']) > 0:
            res['xt'] = datetime.datetime.utcfromtimestamp(float(depth['bids'][0]['timestamp']))
            res['bids'] = [{'price': float(e['price']), 'size': float(e['amount']),\
             'timestamp':float(e['timestamp'])} for e in depth['bids']]
        return res if len(res['bids'])>0 or len(res['asks'])>0 else None

    @staticmethod
    def create():
        return Bitfinex()

Market.register_market(Bitfinex)

if __name__ == "__main__":
    market = Market.get_market('Bitfinex')
    print(market.get_ticker())
