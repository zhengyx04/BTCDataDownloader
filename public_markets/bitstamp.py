import urllib.request
import urllib.error
import urllib.parse
import json
import sys
import datetime
from .market import Market


class Bitstamp(Market):
    def __init__(self):
        super().__init__()
        self.get_api_url='https://www.bitstamp.net/api/v2/order_book/{ticker:s}/'

    def __get_order_book(self,ticker):
        url=self.get_api_url.format(ticker=ticker)
        req = urllib.request.Request(url, None, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode('utf8'))
        return depth

    def get_exchange_depth(self,ticker):
        depth = self.__get_order_book(ticker)
        return self.depth_transform(depth)

    def depth_transform(self,depth):
        res={'xt':datetime.datetime.utcfromtimestamp(float(depth['timestamp']))}
        res['asks'] = [{'price':float(e[0]),'size':float(e[1])}for e in depth['asks']]
        res['bids'] = [{'price':float(e[0]),'size':float(e[1])}for e in depth['bids']]
        return res

    @staticmethod
    def create():
        return Bitstamp()

Market.register_market(Bitstamp)


if __name__ == "__main__":
    market = Market.get_market('Bitstamp')
    print(market.get_ticker())