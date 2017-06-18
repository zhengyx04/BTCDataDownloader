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
        self.update_rate = 1
        self.depth = {}

    def get_orderBook_by_prod(self,prod):
        url = 'https://api.bitfinex.com/v1/book/'
        res = urllib.request.urlopen(url+prod+'?limit_bids=20&limit_asks=20').read().decode('utf8')
        return json.loads(res)

    def get_currency_pair(self,ticker):
        return ticker[0:-3],ticker[-3:]

    def get_exchange_depth(self,ticker):
        depth=self.get_orderBook_by_prod(ticker)
        return self.depth_transform(depth)

    def depth_transform(self,depth):
        res={'xt':datetime.datetime.utcfromtimestamp(float(depth['asks'][0]['timestamp']))}
        res['asks']=[ {'price':float(e['price']),'size':float(e['amount']),'timestamp':float(e['timestamp'])} for e in depth['asks']]
        res['bids'] = [{'price': float(e['price']), 'size': float(e['amount']), 'timestamp':float(
            e['timestamp'])} for e in depth['bids']]
        return res

    @staticmethod
    def create():
        return Bitfinex()

Market.register_market(Bitfinex)

if __name__ == "__main__":
    market = Market.get_market('Bitfinex')
    print(market.get_ticker())
