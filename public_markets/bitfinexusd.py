import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class BitfinexUSD(Market):
    def __init__(self):
        super().__init__("USD")
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def update_depth(self):
        res = urllib.request.urlopen(
            'https://api.bitfinex.com/v1/book/btcusd')
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
        return {'asks':self.get_latest_depth(depth['asks']),'bids':self.get_latest_depth(depth['bids'])}

    @staticmethod
    def create():
        return BitfinexUSD()

Market.register_market(BitfinexUSD)

if __name__ == "__main__":
    market = Market.get_market('BitfinexUSD')
    print(market.get_ticker())
