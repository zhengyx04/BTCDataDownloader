import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class Kraken(Market):
    def __init__(self):
        super().__init__()
        self.get_api_url_orderbook = 'https://api.kraken.com/0/public/Depth?pair={ticker:s}'

    def get_orderBook_by_prod(self,prod):
        url=self.get_api_url_orderbook.format(ticker=prod)
        res = urllib.request.urlopen(url).read().decode('utf8')
        return json.loads(res)

    def get_exchange_depth(self,ticker):
        xt=datetime.datetime.utcnow()
        depth=self.get_orderBook_by_prod(ticker)
        depth=self.depth_transform(xt,depth['result'][ticker])
        return depth

    def depth_transform(self,xt,depth):
        res={'xt':xt}
        if len(depth['asks'])>0:
            res['xt']=datetime.datetime.utcfromtimestamp(depth['asks'][0][2])
            res['asks'] = [{'price': float(e[0]), 'size': float(e[1])} for e in depth['asks']]
        else:
            res['asks'] = []

        if len(depth['bids'])>0:
            res['xt']=datetime.datetime.utcfromtimestamp(depth['bids'][0][2])
            res['bids'] = [{'price': float(e[0]), 'size': float(e[1])} for e in depth['bids']]
        else:
            res['bids'] = []

        return res if len(res['bids'])>0 or len(res['asks'])>0 else None

    @staticmethod
    def create():
        return Kraken()

Market.register_market(Kraken)

if __name__ == "__main__":
    market = Market.get_market('Kraken')
    print(market.get_ticker())
