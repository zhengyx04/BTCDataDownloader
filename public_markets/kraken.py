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
        depth=self.get_orderBook_by_prod(ticker)
        depth=self.depth_transform(depth['result'][ticker])
        return depth

    def depth_transform(self,depth):
        res={'xt':datetime.datetime.utcfromtimestamp(float(depth['asks'][0][2]))}
        res['asks']=[{'price':float(e[0]),'size':float(e[1]),'timestamp':e[2]} for e in depth['asks']]
        res['bids'] = [{'price':float(e[0]),'size':float(e[1]),'timestamp':e[2]} for e in depth['bids']]
        return res

    @staticmethod
    def create():
        return Kraken()

Market.register_market(Kraken)

if __name__ == "__main__":
    market = Market.get_market('Kraken')
    print(market.get_ticker())
