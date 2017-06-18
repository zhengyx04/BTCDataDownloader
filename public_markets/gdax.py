import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class GDAX(Market):
    def __init__(self):
        super().__init__()

    def get_orderBook_by_prod(self,prod):
        url = 'https://api.gdax.com/products/'
        res = urllib.request.urlopen(url+prod+'/book?level=2').read().decode('utf8')
        depths = json.loads(res)
        depths = {'asks':depths['asks'][0:20], 'bids':depths['asks'][0:20], 'sequence':depths['sequence']}
        return depths

    def get_currency_pair(self,ticker):
        return ticker.split('-')

    def get_exchange_depth(self,ticker):
        xt=datetime.datetime.utcnow()
        depth=self.get_orderBook_by_prod(ticker)
        return self.depth_transform(xt,depth)

    def depth_transform(self,xt,depth):
        res={'xt':xt}
        res['asks'] = [{'price':e[0],'size':e[1],'other':e[2]} for e in depth['asks']]
        res['bids'] = [{'price':e[0],'size':e[1],'other':e[2]} for e in depth['bids']]
        return res

    @staticmethod
    def create():
        return GDAX()

Market.register_market(GDAX)

if __name__ == "__main__":
    market = Market.get_market('GDAX')
    print(market.get_ticker())
