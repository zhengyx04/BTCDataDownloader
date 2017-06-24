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
        self.get_api_url_orderbook='https://api.gdax.com/products/{ticker:s}/book?level=2'

    def get_exchange_depth(self,ticker):
        xt=datetime.datetime.utcnow()
        url = self.get_api_url_orderbook.format(ticker=ticker)
        res = urllib.request.urlopen(url).read().decode('utf8')
        depth = json.loads(res)
        depth = {'asks':depths['asks'][0:20], 'bids':depths['asks'][0:20], 'sequence':depths['sequence']}
        return self.depth_transform(xt,depth)

    def depth_transform(self,xt,depth):
        res={'xt':xt, 'asks':[], 'bids':[]}
        if len(depth['asks']) > 0:
            res['asks'] = [{'price':e[0],'size':e[1],'other':e[2]} for e in depth['asks']]
        if len(depth['bids']) > 0:
            res['bids'] = [{'price':e[0],'size':e[1],'other':e[2]} for e in depth['bids']]
        return res if len(res['bids'])>0 or len(res['asks'])>0 else None

    @staticmethod
    def create():
        return GDAX()

Market.register_market(GDAX)

if __name__ == "__main__":
    market = Market.get_market('GDAX')
    print(market.get_ticker())
