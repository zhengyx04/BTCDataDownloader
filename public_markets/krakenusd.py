import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class KrakenUSD(Market):
    def __init__(self):
        super().__init__()
        self.update_rate = 20
        self.depth = {}

    def get_orderBook_by_prod(self,prod):
        url = 'https://api.kraken.com/0/public/Depth?pair='
        res = urllib.request.urlopen(url+prod+'&count=20').read().decode('utf8')
        return json.loads(res)

    def get_orderBook(self,prodList=['XXBTZUSD']):
        return [self.get_orderBook_by_prod(e) for e in prodList]

    def update_depth(self):
        try:
            depth = self.get_orderBook()
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
        self.depth = [self.format_depth(e) for e in depth]

    def format_depth(self,depth):
        prod = list((depth['result']).keys())[0]
        xt=datetime.datetime.utcfromtimestamp(float(depth['result'][prod]['asks'][0][2]))
        lu=datetime.datetime.utcnow()
        date=datetime.datetime.now().strftime('%Y.%m.%d')
        qv=True        
        pccy = prod[-3:]
        occy = prod[2:5]
        _id=self.gen_id(lu,occy+'_'+pccy)
        return {'_id':_id,'date':date,'xt':xt,'lu':lu,'qv':qv,'occy':occy,'pccy':pccy,\
                'asks':self.__format_bidasks(depth['result'][prod]['asks']),\
                'bids':self.__format_bidasks(depth['result'][prod]['bids'])}

    def __format_bidasks(self,bidask):
        return [{'price':float(e[0]),'size':float(e[1])} for e in bidask]


    @staticmethod
    def create():
        return KrakenUSD()

Market.register_market(KrakenUSD)

if __name__ == "__main__":
    market = Market.get_market('KrakenUSD')
    print(market.get_ticker())
