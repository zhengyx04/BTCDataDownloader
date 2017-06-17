import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class BitfinexUSD(Market):
    def __init__(self):
        super().__init__()
        self.update_rate = 20
        self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
            {'price': 0, 'amount': 0}]}

    def get_orderBook_by_prod(self,prod):
        url = 'https://api.bitfinex.com/v1/book/'
        res = urllib.request.urlopen(url+prod+'?limit_bids=20&limit_asks=20').read().decode('utf8')
        return json.loads(res)

    def get_orderBook(self,prodList=['btcusd']):
        return [{e:self.get_orderBook_by_prod(e)} for e in prodList]

    def update_depth(self):
        try:
            depth = self.get_orderBook()
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
        self.depth = [self.format_depth(e) for e in depth]

    def format_depth(self,depth):
        #print(depth)
        prod = list(depth.keys())[0]
        #print(depth[prod]['sequence'])
        xt=datetime.datetime.utcfromtimestamp(float(depth[prod]['asks'][0]['timestamp']))
        lu=datetime.datetime.utcnow()
        date=datetime.datetime.now().strftime('%Y.%m.%d')
        qv=True        
        pccy = prod[-3:]
        occy = prod[0:3]
        _id=self.gen_id(lu,occy+'_'+pccy)
        return {'_id':_id,'date':date,'xt':xt,'lu':lu,'qv':qv,'occy':occy,'pccy':pccy,\
                'asks':self.__format_bidasks(depth[prod]['asks']),\
                'bids':self.__format_bidasks(depth[prod]['bids'])}

    def __format_bidasks(self,bidask):
        return [{'price':float(e['price']),'size':float(e['amount'])} for e in bidask]

    @staticmethod
    def create():
        return BitfinexUSD()

Market.register_market(BitfinexUSD)

if __name__ == "__main__":
    market = Market.get_market('BitfinexUSD')
    print(market.get_ticker())
