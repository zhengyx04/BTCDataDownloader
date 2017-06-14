import urllib.request
import urllib.error
import urllib.parse
import json
import sys
import datetime
from .market import Market


class BitstampUSD(Market):
    def __init__(self):
        super(BitstampUSD, self).__init__()
        self.update_rate = 20

    def update_depth(self):
        url = 'https://www.bitstamp.net/api/order_book/'
        req = urllib.request.Request(url, None, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode('utf8'))
        self.depth = self.format_depth(depth)
        self.depth['date'] = datetime.datetime.now().date()
        utctime=datetime.datetime.utcnow()
        self.depth['lu'] = utctime
        self.depth['asks'][0]['datetime'] = utctime
        self.depth['asks'][0]['timestamp'] = utctime.timestamp()


    @staticmethod
    def create():
        return BitstampUSD()

Market.register_market(BitstampUSD)


if __name__ == "__main__":
    market = Market.get_market('BitstampUSD')
    print(market.get_ticker())