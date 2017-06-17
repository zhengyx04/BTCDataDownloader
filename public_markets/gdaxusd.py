import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import datetime
from .market import Market


class GDAXUSD(Market):
    def __init__(self):
        super().__init__()
        self.update_rate = 20
        self.depth = {}

    def get_orderBook_by_prod(self,prod):
        url = 'https://api.gdax.com/products/'
        res = urllib.request.urlopen(url+prod+'/book?level=2').read().decode('utf8')
        depths = json.loads(res)
        depths = {'asks':depths['asks'][0:20], 'bids':depths['asks'][0:20], 'sequence':depths['sequence']}
        return depths

    def get_orderBook(self,prodList=['BTC-USD']):
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
        xt=datetime.datetime.utcfromtimestamp(float(depth[prod]['sequence']))
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
        return [{'price':float(e[0]),'size':float(e[1])} for e in bidask]

    @staticmethod
    def create():
        return GDAXUSD()

Market.register_market(GDAXUSD)

if __name__ == "__main__":
    market = Market.get_market('GDAXUSD')
    print(market.get_ticker())
