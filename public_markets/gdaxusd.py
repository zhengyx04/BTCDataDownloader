import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class GDAXUSD(Market):
    def __init__(self):
        super().__init__("USD")
        self.update_rate = 20
        self.depth = {}

    def update_depth(self):
        res = urllib.request.urlopen(
            'https://api.gdax.com/products/BTC-USD/book')
        jsonstr = res.read().decode('utf8')
        try:
            depth = json.loads(jsonstr)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
        self.depth = self.format_depth(depth)

    def get_latest_depth(self,depth):
        for x in depth:
            x['datetime']=datetime.datetime.utcfromtimestamp(int(float(x['timestamp'])))
        depth.sort(key=lambda x:x['datetime'],reverse=True)
        return [depth[0]]

    def format_depth(self,depth):
        return {'date':datetime.datetime.now().date(),'lu':datetime.datetime.utcnow(),\
          'asks':depth['asks'][0],\
          'bids':depth['bids'][0]}

    @staticmethod
    def create():
        return GDAXUSD()

Market.register_market(GDAXUSD)

if __name__ == "__main__":
    market = Market.get_market('GDAXUSD')
    print(market.get_ticker())
